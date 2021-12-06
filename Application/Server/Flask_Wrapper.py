from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import Config

flask_server = Flask(__name__)
auth = HTTPBasicAuth()
flask_server.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY

users={
    "john": generate_password_hash("password")
}

@auth.verify_password
def Verify_Password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Device Management System'
    }
)
flask_server.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from Command import HTTP_Command_Handler