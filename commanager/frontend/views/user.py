"""
Commanager profile.

URLs include:
/users/<user_url_slug>
"""
import flask
import commanager


@commanager.app.route('/users/<username>/')
def show_user_page(username):
    """Display /users/user route."""
    if  'user' not in flask.session:
        return flask.redirect('/login')
    
    name = flask.session['name']
    username = flask.session['username']
    
    context = {
        "username": username,
        "name": name,
    }

    return flask.render_template("user.html", **context)