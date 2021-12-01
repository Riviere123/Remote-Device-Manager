from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import Config

flask_server = Flask(__name__)
flask_server.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY

@flask_server.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

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