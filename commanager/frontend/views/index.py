"""
eecs497 main view.

URLs include:
/
"""
import flask
import commanager


@commanager.app.route('/')
def show_index():
    """Display / route."""
    if  'user' not in flask.session:
        return flask.redirect('/login')
    
    name = flask.session['name']
    username = flask.session['username']

    context = {
        "username": username,
        "name": name
    }

    return flask.render_template("index.html", **context)
