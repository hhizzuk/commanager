from flask import render_template, session, redirect, url_for, abort
from supabase import create_client
from commanager.server import config
supabase_admin = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
supabase_user = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def get_authorized_user():
    if 'username' not in session:
        return None
    return session['username']

def setup_page_routes(app):
    @app.route('/')
    def home():
        if not (username := get_authorized_user()):
            return redirect(url_for('login'))

        services = supabase_user.table('services').select('*').execute().data or []
        users = supabase_user.table('users').select('uid, username').execute().data or []

        uid_to_username = {str(user['uid']): user['username'] for user in users}

        for service in services:
            service_uid = str(service['uid'])
            service['username'] = uid_to_username.get(service_uid, 'unknown')
            print(f"[DEBUG] {service['title']} by UID {service_uid} → {service['username']}")

        return render_template('home.html', username=username, services=services)

    @app.route('/user/<username>/')
    def user_profile(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        # 🔍 Fetch user data by username
        user_data = supabase_admin.table('users') .select('uid', 'pfp', 'rating', 'bio', 'social_media_links', 'email').eq('username', username).single().execute()

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
        return render_template('messages.html', username=current_user)

    @app.route('/user/<username>/orders')
    def user_orders(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)
        return render_template('orders.html', username=current_user)

    @app.route('/payment')
    def payment():
        if not (username := get_authorized_user()):
            return redirect(url_for('login'))
        return render_template('payment.html', username=username)

    @app.route('/request')
    def request_page():
        if not (username := get_authorized_user()):
            return redirect(url_for('login'))
        return render_template('request.html', username=username)

    @app.route('/user/<username>/settings')
    def user_settings(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)
        return render_template('settings.html', username=current_user)

    @app.context_processor
    def inject_user_pfp():
        if 'user' not in session:
            return {}

        uid = session['user']
        try:
            user_data = supabase_user.table('users').select('pfp').eq('uid', uid).single().execute()
            return {'pfp': user_data.data.get('pfp', None)}
        except Exception:
            return {'pfp': None}