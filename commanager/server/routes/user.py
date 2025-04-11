from flask import request, render_template, redirect, jsonify, session
from supabase import create_client
from commanager.server import config

supabase_admin = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
supabase_user = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def setup_user_routes(app):
    @app.route('/update_password', methods=['POST'])
    def update_password():
        if 'user' not in session:
            return jsonify({'error': 'Not logged in'}), 401
            
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not all([current_password, new_password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            # Get user email from database
            user_data = supabase_admin.table('users').select('email').eq('uid', session['user']).single().execute()
            user_email = user_data.data['email']
            
            # Verify current password
            supabase_user.auth.sign_in_with_password({
                'email': user_email,
                'password': current_password
            })
            
            # Update password
            supabase_admin.auth.admin.update_user_by_id(
                session['user'],
                {'password': new_password}
            )
            
            return jsonify({'message': 'Password updated successfully'})
            
        except Exception as e:
            return jsonify({'error': 'Invalid current password or other error'}), 400

    @app.route('/user/<user_url_slug>/', methods=['GET'])
    def display_user(user_url_slug):
        """Display /users/user route."""
        if  'user' not in session:
            return redirect('/login')
        
        uid = session['user']
        username = session['username']
        user_data = supabase_user.table('users').select('profile_urls', 'pfp', 'rating', 'bio', 'social_media_links', 'email').eq('uid', uid).single().execute()
        services = supabase_user.table('services').select('*').eq('uid', uid).single().execute()
        reviews = supabase_user.table('reviews').select('*').eq('reviewee_id', uid).single().execute()
        portfolio = user_data['profile_urls']
        pfp = user_data['pfp']
        bio = user_data['bio']
        sm_links = user_data['social_media_links']
        email = user_data['email']
        rating = user_data['rating']
        
        context = {
            "uid": uid,
            "username": username,
            "pfp": pfp,
            "bio": bio,
            "sm_links": sm_links,
            "email": email,
            "services": services,
            "portfolio": portfolio,
            "reviews": reviews,
            "rating": rating
        }

        return render_template("user.html", **context)
    
    # @app.route('/user/<user_url_slug>/', methods=['POST'])
    # def update_services():
    #     target_url = request.args.get('target')
    #     return redirect(target_url)