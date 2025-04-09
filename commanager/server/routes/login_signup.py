from flask import request, redirect, url_for, render_template, flash, session
from supabase import create_client, Client
from commanager.server import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def setup_routes(app):
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('Passwords do not match.')
                return render_template('signup.html')

            result = supabase.auth.sign_up({'email': email, 'password': password})
            if result.get('error'):
                flash('Signup failed: ' + result['error']['message'])
                return render_template('signup.html')

            uid = result['user']['id']
            supabase.table('users').insert({
                'uid': uid,
                'username': username,
                'email': email,
                'pfp': '',
                'bio': '',
                'sid': '',
                'social_media_links': {},
                'created_at': None,
                'type': 'standard',
                'profile_urls': [],
                'rating': 0.0
            }).execute()

            flash('Signup successful!')
            return render_template('home.html')

        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            result = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            if result.get('error'):
                flash('Login failed: ' + result['error']['message'])
            else:
                session['user'] = result['session']['access_token']
                flash('Logged in successfully!')
                return redirect(url_for('dashboard'))
        return render_template('login.html')
