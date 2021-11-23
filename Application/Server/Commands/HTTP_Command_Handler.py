from typing import List
from Flask_Wrapper import flask_server
from flask import jsonify, request
from Commands.Command_Handler import Command_Handler, Command
from flask_restplus import Api

# class HTTP_Command_Handler():
#     @flask_server.route('/<string:command>/<string:argument1>/<string:argument2>')
#     @flask_server.route('/<string:command>/<string:argument1>/', defaults={"argument2":""})
#     @flask_server.route('/<string:command>/',defaults={'argument1':"", "argument2":""})
#     @flask_server.route('/',defaults={"command":"", "argument1":"", "argument2":""})
#     def HTTP_Handler(command, argument1, argument2):
#         if(command != ""):
#             command = command.lower().split('_')
#             length,command = Command_Handler.Check_For_Server_Command(command)
#             if command == None:
#                 return("Invalid Command")
#             argument1 = [argument1.lower()]
#             argument2 = argument2.lower().split("_")
#             arguments = argument1 + argument2
#             return(jsonify(f"{Command_Handler.Process_Command(command, arguments)}"))
#         else:
#             return("The server is live! this is the homepage!")
class HTTP_Command_Handler():
    @flask_server.route('/', methods=["GET","POST","DELETE"])
    def Index():
        if request.method == 'GET':
            return(jsonify({"message":"Server is live!"}))
        if request.method == "POST":
            command = request.form.get('command')

    

    @flask_server.route('/devices', methods=["GET"])
    def List_Devices():
        devices = Command.List()
        return(jsonify(devices))
    @flask_server.route('/groups', methods=["GET"])
    def List_Groups():
        groups = Command.Group_List()
        return(jsonify(groups))
