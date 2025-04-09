# """Commanager functions."""
# import flask
# import commanager


# def connect_and_login():
#     """Get (Response, connection, username) as output."""
#     conn = commanager.model.get_db()

#     if 'username' not in flask.session:
#         return None, None, flask.redirect(flask.url_for('login'))
    
#     username = flask.session['username']
#     return None, conn, username
