from flask import Flask
import Config
flask_server = Flask(__name__)
flask_server.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY
from Commands.HTTP_Command_Handler import HTTP_Command_Handler