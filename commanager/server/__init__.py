"""eecs497 package initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('commanager.server.config')

# import commanager.api
# import commanager.views
import commanager.server.model
