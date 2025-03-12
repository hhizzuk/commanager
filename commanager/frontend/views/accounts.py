"""Commanager account operations/routes."""
import flask
import commanager


def login_func(connection):
    0


def create_func(connection):
    """Create account."""
    0


def delete_func(connection):
    """Delete account."""
    if 'logname' not in flask.session:
        flask.abort(403)
    logname = flask.session['logname']
    
    #delete from  db

    cur = connection.execute(
        "delete from users where username=?",
        (logname, )
    )
    flask.session.clear()


def edit_account_func(connection):
    """Edit account."""
    if 'logname' not in flask.session:
        flask.abort(403)
    logname = flask.session['logname']

    #change username, commlist, fullname


def update_password_func(connection):
    0


@commanager.app.route('/accounts/logout/', methods=['POST'])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))


@commanager.app.route('/accounts/', methods=['POST'])
def update_accounts():
    connection = commanager.model.get_db()
    function = flask.request.form.get('function')
    if function == 'login':
        login_func(connection)

    elif function == 'create':
        create_func(connection)

    elif function == 'delete':
        delete_func(connection)

    elif function == 'edit_account':
        edit_account_func(connection)

    elif function == 'update_password':
        update_password_func(connection)

    return flask.get_redirect(flask.url_for('show_index'))


@commanager.app.route('/accounts/login/', methods=['GET'])
def login():
    if 'logname' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template('login.html')


@commanager.app.route('/accounts/create/', methods=['GET'])
def create_account():
    if 'logname' in flask.session:
        return flask.redirect(flask.url_for('edit_account'))
    return flask.render_template('create.html')


@commanager.app.route('/accounts/delete/', methods=['GET'])
def delete_account():
    if 'logname' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    context = {"logname": flask.session['logname']}
    return flask.render_template('delete.html', **context)


@commanager.app.route('/accounts/edit/', methods=['GET'])
def edit_account():
    0


@commanager.app.route('/accounts/auth/', methods=['GET'])
def auth():
    if 'logname' in flask.session:
        return '', 200
    flask.abort(403)