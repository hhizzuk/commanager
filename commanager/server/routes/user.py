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
            user_data = supabase_admin.table('users').select('email').eq('uid', session['user']).single().execute()
            user_email = user_data.data['email']

            supabase_user.auth.sign_in_with_password({
                'email': user_email,
                'password': current_password
            })

            supabase_admin.auth.admin.update_user_by_id(
                session['user'],
                {'password': new_password}
            )

            return jsonify({'message': 'Password updated successfully'})

        except Exception:
            return jsonify({'error': 'Invalid current password or other error'}), 400

    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        uid = session['user']
        bio = request.form.get('bio', '')
        sm_links = request.form.get('social_links', '')
        file = request.files.get('profile_picture')
        profile_pic_url = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('commanager', 'server', 'static', 'uploads', 'pfps')
            os.makedirs(upload_path, exist_ok=True)
            profile_pic_url = f"/static/uploads/pfps/{filename}"
            file.save(os.path.join(upload_path, filename))

        updates = {
            'bio': bio,
            'social_media_links': sm_links,
        }
        if profile_pic_url:
            updates['pfp'] = profile_pic_url

        supabase_user.table('users').update(updates).eq('uid', uid).execute()

        return redirect(url_for('user_profile', username=current_user))

    @app.route('/add_service', methods=['POST'])
    def add_service():
        if not (current_user := get_authorized_user()):
            return redirect(url_for('login'))

        uid = session['user']
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price') or "N/A"
        file = request.files.get('image')
        service_image_url = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('commanager', 'server', 'static', 'uploads', 'services')
            os.makedirs(upload_path, exist_ok=True)
            service_image_url = f"/static/uploads/services/{filename}"
            try:
                file.save(os.path.join(upload_path, filename))
            except Exception as e:
                print("File save error:", e)
                return jsonify({'error': f'File save error: {str(e)}'}), 400

        service_data = {
            'uid': uid,
            'title': title,
            'description': description,
            'price': price,
            'image_urls': [service_image_url] if service_image_url else [],
        }

        supabase_user.table('services').insert(service_data).execute()

        return redirect(url_for('user_profile', username=current_user))

    @app.route('/add_portfolio', methods=['POST'])
    def add_portfolio():
        if not (current_user := get_authorized_user()):
            return jsonify({'error': 'User not authorized'}), 401

        uid = session['user']
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('image')
        portfolio_image_url = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('commanager', 'server', 'static', 'uploads', 'portfolio')
            os.makedirs(upload_path, exist_ok=True)
            portfolio_image_url = f"/static/uploads/portfolio/{filename}"
            file.save(os.path.join(upload_path, filename))

        portfolio_data = {
            'uid': uid,
            'title': title,
            'description': description,
            'img': portfolio_image_url,
        }

        supabase_user.table('portfolio').insert(portfolio_data).execute()

        return redirect(url_for('user_profile', username=current_user))

    @app.route('/edit_portfolio', methods=['POST'])
    def edit_portfolio():
        if not (current_user := get_authorized_user()):
            return jsonify({'error': 'User not authorized'}), 401

        uid = session['user']
        portfolio_id = request.form.get('portfolio_id')
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('image')

        portfolio_item = supabase_user.table('portfolio').select('*').eq('pid', portfolio_id).eq('uid', uid).execute()
        if not portfolio_item.data:
            return jsonify({'error': 'Portfolio item not found or unauthorized'}), 404

        update_data = {
            'title': title,
            'description': description,
        }

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join('commanager', 'server', 'static', 'uploads', 'portfolio')
            os.makedirs(upload_path, exist_ok=True)
            portfolio_image_url = f"/static/uploads/portfolio/{filename}"
            file.save(os.path.join(upload_path, filename))
            update_data['img'] = portfolio_image_url

        supabase_user.table('portfolio').update(update_data).eq('pid', portfolio_id).eq('uid', uid).execute()

        return redirect(url_for('user_profile', username=current_user))

    @app.route('/delete_portfolio/<portfolio_id>', methods=['POST'])
    def delete_portfolio(portfolio_id):
        if not (current_user := get_authorized_user()):
            return jsonify({'error': 'User not authorized'}), 401

        uid = session['user']
        portfolio_item = supabase_user.table('portfolio').select('*').eq('pid', portfolio_id).eq('uid', uid).execute()
        if not portfolio_item.data:
            return jsonify({'error': 'Portfolio item not found or unauthorized'}), 404

        supabase_user.table('portfolio').delete().eq('pid', portfolio_id).eq('uid', uid).execute()

        return jsonify({'message': 'Portfolio item deleted successfully'})
