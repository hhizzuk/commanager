from flask import request, redirect, url_for, render_template, session
from supabase import create_client, Client
from commanager.server import config
import time

supabase_admin: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)

def setup_destroy_routes(app):
    @app.route('/destroy_account', methods=['GET', 'POST'])
    def destroy_account():
        if 'user' not in session:
            return redirect(url_for('login'))

        if request.method == 'POST':
            try:
                user_id = session['user']
                username = session.get('username')

                # 1. First delete the auth user (MOST IMPORTANT)
                try:
                    # This is the crucial line that actually prevents future logins
                    auth_response = supabase_admin.auth.admin.delete_user(user_id)
                    if not auth_response:
                        raise Exception("Failed to delete auth user")
                except Exception as auth_error:
                    print(f"Auth deletion error: {auth_error}")
                    raise Exception("Could not remove authentication record")

                # 2. Delete from users table
                supabase_admin.table('users').delete().eq('uid', user_id).execute()

                # 3. Clean up related data (optional but recommended)
                related_tables = ['services', 'portfolio', 'reviews', 'orders']
                for table in related_tables:
                    try:
                        supabase_admin.table(table).delete().or_(
                            f"uid.eq.{user_id}",
                            f"artist_id.eq.{user_id}",
                            f"client_id.eq.{user_id}"
                        ).execute()
                        time.sleep(0.1)
                    except:
                        continue

                # 4. Clear session
                session.clear()

                # 5. Return to login with success message
                return redirect(url_for('login', deleted=True))

            except Exception as e:
                print(f"Account deletion failed: {str(e)}")
                return render_template('settings.html', 
                                    current_user=username,
                                    error_message="Failed to delete account. Please contact support.")

        # GET request - show confirmation page
        return render_template('destroy_account.html')