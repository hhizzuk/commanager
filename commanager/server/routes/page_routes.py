from flask import render_template, session, redirect, url_for

def setup_page_routes(app):
    @app.route('/')
    def home():
        username = session.get('username')
        print("Session username on home route:", session.get('username'))
        if not username:
            return redirect(url_for('login'))
        return render_template('home.html', username=username)

    @app.route('/user/<username>/')
    def user_profile(username):
        username = session.get('username')
        return render_template('user.html', username=username)

    @app.route('/user/<username>/messages')
    def user_messages(username):
        username = session.get('username')
        return render_template('messages.html', username=username)

    @app.route('/user/<username>/orders')
    def user_orders(username):
        username = session.get('username')
        return render_template('orders.html', username=username)

    @app.route('/payment')
    def payment():
        username = session.get('username')
        return render_template('payment.html')

    @app.route('/request')
    def request_page():
        username = session.get('username')
        return render_template('request.html')

    @app.route('/user/<username>/settings')
    def user_settings(username):
        username = session.get('username')
        return render_template('settings.html', username=username)
