import os
from flask import request, render_template, redirect, jsonify, session, url_for
from supabase import create_client
from commanager.server import config
from commanager.server.routes.page_routes import get_authorized_user
from werkzeug.utils import secure_filename

supabase_admin = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_ROLE_KEY)
supabase_user = create_client(config.SUPABASE_URL, config.SUPABASE_ANON_KEY)

def setup_user_routes(app):
    @app.route('/update_password', methods=['POST'])
    def update_password():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))
            
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


    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        uid = session['user']

        # Get form fields
        bio = request.form.get('bio', '')
        sm_links = request.form.get('social_links', '')

        # Optional file upload
        file = request.files.get('profile_picture')
        profile_pic_url = None

        # If a file was uploaded, handle it (this is a placeholder)
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('commanager', 'server', 'static', 'uploads')
            os.makedirs(upload_path, exist_ok=True)  # Create the folder if needed
            profile_pic_url = f"/static/uploads/{filename}"
            file.save(os.path.join(upload_path, filename))

        # Build the update payload
        updates = {
            'bio': bio,
            'social_media_links': sm_links,
        }
        if profile_pic_url:
            updates['pfp'] = profile_pic_url

        # Update in Supabase
        response = supabase_user.table('users').update(updates).eq('uid', uid).execute()

        # Refresh session if username or anything else needs updating later
        return redirect(url_for('user_profile', username=current_user))
