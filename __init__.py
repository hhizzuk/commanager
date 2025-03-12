"""eecs497 package initializer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('config')

app.config.from_envvar('INSTA485_SETTINGS', silent=True)

import insta485.api
import insta485.views
import insta485.model
