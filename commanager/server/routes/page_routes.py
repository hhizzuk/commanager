from flask import render_template

def setup_page_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/user/<username>/')
    def user_profile(username):
        return render_template('user.html', username=username)

    @app.route('/user/<username>/messages')
    def user_messages(username):
        return render_template('messages.html', username=username)

    @app.route('/user/<username>/orders')
    def user_orders(username):
        return render_template('orders.html', username=username)

    @app.route('/payment')
    def payment():
        return render_template('payment.html')

    @app.route('/request')
    def request_page():
        return render_template('request.html')

    @app.route('/user/<username>/settings')
    def user_settings(username):
        return render_template('settings.html', username=username)
