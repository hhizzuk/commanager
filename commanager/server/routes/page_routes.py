from flask import render_template, session, redirect, url_for, abort

def setup_page_routes(app):
    def get_authorized_user():
        if 'username' not in session:
            return None
        return session['username']
    
    @app.route('/')
    def home():
        if not (username := get_authorized_user()):
            return redirect(url_for('login'))
        return render_template('home.html', username=username)

    @app.route('/user/<username>/')
    def user_profile(username):
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
        if username != current_user:
            abort(403)  # Forbidden if accessing other user's profile
        return render_template('user.html', username=current_user)

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