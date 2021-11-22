from Flask_Wrapper import flask_server
from flask import jsonify
from Commands.Command_Handler import Command_Handler

class HTTP_Command_Handler():
    @flask_server.route('/<string:command>/<string:argument1>/<string:argument2>')
    @flask_server.route('/<string:command>/<string:argument1>/', defaults={"argument2":""})
    @flask_server.route('/<string:command>/',defaults={'argument1':"", "argument2":""})
    @flask_server.route('/',defaults={"command":"", "argument1":"", "argument2":""})
    def HTTP_Handler(command, argument1, argument2):
        if(command != ""):
            command = command.lower().split('_')
            length,command = Command_Handler.Check_For_Server_Command(command)
            argument1 = [argument1.lower()]
            argument2 = argument2.lower().split("_")
            arguments = argument1 + argument2
            return(f"{Command_Handler.Process_Command(command, arguments)}")
        else:
            return("The server is live! this is the homepage!")

