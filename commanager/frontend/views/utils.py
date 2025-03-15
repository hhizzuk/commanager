"""Commanager functions."""
import flask
import commanager


def get_connection_and_logname():
    """Get (Response, connection, username) as output."""
    conn = commanager.model.get_db()

    if 'username' not in flask.session:
        return None, None, flask.redirect(flask.url_for('login'))
    
    username = flask.session['username']
    return None, conn, username
