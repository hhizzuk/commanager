from flask import request, redirect, url_for, render_template, flash, session
from supabase import create_client, Client
from commanager.server import config

supabase_admin: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
supabase_user: Client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def setup_routes(app):
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                return render_template('signup.html', popup_message="Passwords do not match.")
            try:
                response = supabase_admin.auth.admin.create_user({
                    'email': email.strip(),
                    'password': password,
                    'email_confirm': True
                })
                user = response.user
            except Exception as e:
                import traceback
                traceback.print_exc()
                flash(f'Signup failed: {e}')
                return render_template('signup.html')

            uid = user.id
            supabase_admin.table('users').update({
                'username': username,
                'pfp': '',
                'bio': '',
                'sid': '',
                'social_media_links': {},
                'created_at': None,
                'profile_urls': [],
                'rating': 0.0
            }).eq('uid', uid).execute()

            session['user'] = uid
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                result = supabase_user.auth.sign_in_with_password({
                    'email': email,
                    'password': password
                })
                
                uid = result.user.id
                session['user'] = uid
                # get the username from the database using the uid
                user_data = supabase_user.table('users').select('username').eq('uid', uid).single().execute()
                username = user_data.data['username']
                session['username'] = username

                return redirect(url_for('home'))
            except Exception as e:
                return render_template('login.html', popup_message="Error logging in.")

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))