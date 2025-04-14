from flask import render_template, session, redirect, url_for, abort
from flask import request, jsonify
from supabase import create_client
from commanager.server import config

supabase_admin = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
supabase_user = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def get_authorized_user():
    return session.get('username')

def setup_page_routes(app):
    @app.route('/')
    def home():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        services = supabase_user.table('services').select('*').execute().data or []
        users = supabase_user.table('users').select('uid, username').execute().data or []

        uid_to_username = {str(user['uid']): user['username'] for user in users}

        for service in services:
            service_uid = str(service['uid'])
            service['username'] = uid_to_username.get(service_uid, 'unknown')
            print(f"[DEBUG] {service['title']} by UID {service_uid} → {service['username']}")

        return render_template('home.html', current_user=current_user, services=services)

    @app.route('/user/<username>/')
    def user_profile(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        # 🔍 Fetch user data by username
        user_data = supabase_admin.table('users') \
            .select('uid', 'pfp', 'rating', 'bio', 'social_media_links', 'email') \
            .eq('username', username).single().execute()

        if not user_data.data:
            abort(404, description="User not found")

        uid = user_data.data['uid']

        services = supabase_user.table('services').select('*').eq('uid', uid).execute().data or []
        portfolio = supabase_user.table('portfolio').select('*').eq('uid', uid).execute().data or []
        reviews = supabase_user.table('reviews').select('*').eq('reviewee_id', uid).execute().data or []

        context = {
            "uid": uid,
            "pfp": user_data.data['pfp'],
            "bio": user_data.data['bio'],
            "sm_links": user_data.data['social_media_links'],
            "email": user_data.data['email'],
            "services": services,
            "portfolio": portfolio,
            "reviews": reviews,
            "rating": user_data.data['rating']
        }

        return render_template('user.html', **context, username=username, current_user=current_user)

    @app.route('/user/<username>/messages')
    def user_messages(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)
        return render_template('messages.html', current_user=current_user)

    @app.route('/user/<username>/orders')
    def user_orders(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)
        return render_template('orders.html', current_user=current_user)

    @app.route('/payment')
    def payment():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        return render_template('payment.html', current_user=current_user)

    @app.route('/request')
    def request_page():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        return render_template('request.html', current_user=current_user)

    @app.route('/user/<username>/settings')
    def user_settings(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)
        return render_template('settings.html', current_user=current_user)

    @app.context_processor
    def inject_user_pfp():
        """
        Injects the logged-in user's profile picture into templates under 'my_pfp'.
        The profile picture of the user being viewed is passed separately in context (e.g., in user_profile).
        """
        if 'user' not in session:
            return {}
        
        uid = session['user']
        try:
            user_data = supabase_user.table('users').select('pfp').eq('uid', uid).single().execute()
            return {'my_pfp': user_data.data.get('pfp', None)}
        except Exception:
            return {'my_pfp': None}
        
    @app.route('/submit_review', methods=['POST'])
    def submit_review():
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400

        try:
            data = request.get_json()
            current_user = get_authorized_user()
            
            if not current_user:
                return jsonify({'error': 'Not authorized'}), 401
                
            reviewee_username = data.get('reviewee_username')
            rating = data.get('rating')
            comment = data.get('comment', '')

            # Validate required fields
            if not all([reviewee_username, rating]):
                return jsonify({'error': 'Missing required fields'}), 400

            # Get reviewee data
            reviewee_response = supabase_admin.table('users').select('uid').eq('username', reviewee_username).execute()
            if not reviewee_response.data:
                return jsonify({'error': 'User not found'}), 404
            reviewee_uid = reviewee_response.data[0]['uid']

            # Get reviewer data
            reviewer_response = supabase_admin.table('users').select('uid').eq('username', current_user).execute()
            reviewer_uid = reviewer_response.data[0]['uid']

            # Check if user has ordered from this seller before
            # Get all service IDs (sid) by the reviewee
            services_response = supabase_admin.table('services').select('sid').eq('uid', reviewee_uid).execute()
            service_ids = [service['sid'] for service in services_response.data]
            
            # Check if reviewer has ordered any of these services (using cid in orders table)
            has_ordered = False
            if service_ids:
                orders_response = supabase_admin.table('orders').select('*').eq('client_id', reviewer_uid).in_('cid', service_ids).execute()
                has_ordered = bool(orders_response.data)

            # Prepare review data
            review_data = {
                'reviewer_id': reviewer_uid,
                'reviewee_id': reviewee_uid,
                'rating': int(rating),
                'comment': comment,
                'verified_customer': has_ordered
            }

            # Insert review
            insert_response = supabase_admin.table('reviews').insert(review_data).execute()
            if not insert_response.data:
                raise Exception("Failed to insert review - no data returned")

            # Calculate average rating
            reviews_response = supabase_admin.table('reviews').select('rating').eq('reviewee_id', reviewee_uid).execute()
            ratings = [review['rating'] for review in reviews_response.data]
            avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

            # Update user rating
            supabase_admin.table('users').update({'rating': avg_rating}).eq('uid', reviewee_uid).execute()

            return jsonify({
                'success': True,
                'verified': has_ordered,
                'new_rating': avg_rating
            })

        except Exception as e:
            print(f"Error submitting review: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
    @app.route('/delete_review/<review_id>', methods=['DELETE'])
    def delete_review(review_id):
        try:
            current_user = get_authorized_user()
            if not current_user:
                return jsonify({'error': 'Not authorized'}), 401

            # Get the review to verify ownership
            review_response = supabase_admin.table('reviews').select('*').eq('rid', review_id).execute()
            if not review_response.data:
                return jsonify({'error': 'Review not found'}), 404
                
            review = review_response.data[0]
            reviewer_response = supabase_admin.table('users').select('uid').eq('username', current_user).execute()
            reviewer_uid = reviewer_response.data[0]['uid']

            # Verify the current user is the reviewer
            if review['reviewer_id'] != reviewer_uid:
                return jsonify({'error': 'Not authorized to delete this review'}), 403

            # Delete the review
            delete_response = supabase_admin.table('reviews').delete().eq('rid', review_id).execute()
            
            if not delete_response.data:
                raise Exception("Failed to delete review")

            # Recalculate average rating
            reviewee_uid = review['reviewee_id']
            reviews_response = supabase_admin.table('reviews').select('rating').eq('reviewee_id', reviewee_uid).execute()
            ratings = [r['rating'] for r in reviews_response.data]
            avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

            # Update user rating
            supabase_admin.table('users').update({'rating': avg_rating}).eq('uid', reviewee_uid).execute()

            return jsonify({'success': True, 'new_rating': avg_rating})

        except Exception as e:
            print(f"Error deleting review: {str(e)}")
            return jsonify({'error': str(e)}), 500
