"""
eecs497 main view.

URLs include:
/
"""
import flask
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    redirect_response, connection, logname = get_connection_and_logname()
    if redirect_response is not None:
        return redirect_response

    cur = connection.execute(
        "select postid, owner, filename as img_url, created as timestamp " +
        "from posts " +
        "where owner in ( " +
        "    select username2 " +
        "    from following " +
        "    where username1 = ? or username2 = ? " +
        ") " +
        "order by created DESC, postid DESC ",
        (logname, logname)
    )
    posts = cur.fetchall()
    for post in posts:
        cur = connection.execute(
            "select filename as owner_img_url " +
            "from users " +
            "where username = ? ",
            (post['owner'], )
        )
        post['owner_img_url'] = cur.fetchone()['owner_img_url']
        post['timestamp'] = arrow.get(post['timestamp']).humanize()
        cur = connection.execute(
            "select * " +
            "from comments " +
            "where postid = ? " +
            "order by created desc, commentid desc",
            (post['postid'], )
        )
        post['comments'] = cur.fetchall()
        cur = connection.execute(
            "select count(*) as num " +
            "from likes " +
            "where postid = ? ",
            (post['postid'], )
        )
        post['likes'] = cur.fetchone()['num']
        cur = connection.execute(
            "select count(*) as liked " +
            "from likes " +
            "where postid = ? and owner = ? ",
            (post['postid'], logname)
        )
        post['liked'] = cur.fetchone()['liked']

    # Add database info to context
    context = {
        "logname": logname,
        "posts": posts
    }

    return flask.render_template("index.html", **context)
