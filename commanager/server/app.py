from flask import Flask
from commanager.server import config
from commanager.server.routes.login_signup import setup_routes
from commanager.server.routes.page_routes import setup_page_routes
from commanager.server.routes.destroy_account import setup_destroy_routes
from commanager.server.routes.user import setup_user_routes 

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

setup_routes(app)
setup_page_routes(app)
setup_destroy_routes(app)
setup_user_routes(app)  # Add this line

if __name__ == "__main__":
    app.run(debug=True)