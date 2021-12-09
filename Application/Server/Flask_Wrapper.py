from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import Config

flask_server = Flask(__name__)                               #Flask server object

#NOTE - Will most likely switch to token authentication
auth = HTTPBasicAuth()                                       #Used for basic authentication with the users dictionary below
flask_server.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY  #Sets the flasks form encryption secret key

users={                                                      #NOTE: Temporary dictionary of users/passwords
    "john": generate_password_hash("password")
}

@auth.verify_password
def Verify_Password(username, password):                     #Helper command to pass in the users dictionary to the verify_password wrapper
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

SWAGGER_URL = '/swagger'                                     #The URL for the swagger API docs
API_URL = '/static/swagger.json'                             #The formatting of the swagger page
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Device Management System'
    }
)
flask_server.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)  #Register the swagger extension as a blueprint for flask

from Command import HTTP_Command_Handler