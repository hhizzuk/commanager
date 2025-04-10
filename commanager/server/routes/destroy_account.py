from flask import request, redirect, url_for, render_template, flash, session
from supabase import create_client, Client
from commanager.server import config

supabase_admin: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)

def setup_destroy_routes(app):
    @app.route('/destroy_account', methods = ['GET', 'POST'])
    def destroy_account():
        if 'user' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            try:
                #get user id from session
                user_id = session['user']

                #delete user data from users table
                supabase_admin.table('users').delete().eq('uid', user_id).execute()

                #delete auth user
                supabase_admin.auth.admin.delete_user(user_id)

                #clear session
                session.clear()

                #redirect to login
                return render_template('login.html', popup_message="Account was successfuly deleted.")
            
            except Exception as e:
                #log error for debugging
                print(f"Error deleting account: {e}")
                return render_template('settings.html', username=session.get('username'), 
                                       error_message="Failed to delete account. Please try again.")
       
        #show confirmation page for GET requests
        return render_template('destroy_account.html')
