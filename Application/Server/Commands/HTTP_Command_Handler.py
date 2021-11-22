from typing import Type
from Flask_Wrapper import flask_server
from Commands.Commands import Command
from flask import jsonify
from Commands.Command_Handler import Command_Handler

class HTTP_Command_Handler():
    @flask_server.route('/')
    def Index():
        return "Server Running"


    @flask_server.route('/<string:command>/<string:argument1>/<string:argument2>')
    @flask_server.route('/<string:command>/<string:argument1>/', defaults={"argument2":None})
    @flask_server.route('/<string:command>/',defaults={'argument1':None, "argument2":None})
    def HTTP_Handler(command, argument1, argument2):
        command = Command_Handler.Check_For_Server_Command(command.lower().split("_"))
        if argument1 != None:
            if argument2 != None:
                return command(argument1,argument2)
            else:
                return command(argument1)
        else:
            return command()