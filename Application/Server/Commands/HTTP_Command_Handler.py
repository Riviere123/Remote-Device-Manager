from Flask_Wrapper import flask_server
from flask import jsonify, request
from Commands.Command_Handler import Command_Handler, Command
from Device import Device, Group
import time
class HTTP_Command_Handler():
    @flask_server.route('/', methods=["GET"])
    def Index():
        if request.method == 'GET':
            return(jsonify({"message":"Server is live!"}))

###################DEVICE#################################
    @flask_server.route('/devices', methods=["GET"])
    def HTTP_List_Devices():
        devices = Command.List()
        return(jsonify(devices))
    
    @flask_server.route('/devices/<string:device_id>', methods=["GET", "DELETE"])
    def HTTP_Device(device_id):
        if request.method == 'GET':
            device = Command.Get_Device_By_ID(device_id)
            return(jsonify(device))
        elif request.method == 'DELETE':
            device = Device.devices[device_id]
            message = Command.Delete(device)
            return(jsonify(message))

    @flask_server.route('/devices/<string:device_id>/name', methods=["POST"])
    def HTTP_Device_Name(device_id):
        if request.method == 'POST':
            data = request.json
            name = data["name"]
            device = Device.devices[device_id]
            message = Command.Set_Name(device, name)
            return(jsonify(message))

    @flask_server.route('/devices/<string:device_id>/type', methods=["POST"])
    def HTTP_Device_Type(device_id):
        if request.method == 'POST':
            data = request.json
            new_type = data["type"]
            device = Device.devices[device_id]
            message = Command.Set_Type(device, new_type)
            return(jsonify(message))
    
    @flask_server.route('/devices/<string:device_id>/run', methods=["POST"])
    def HTTP_Device_Run(device_id):
        if request.method == 'POST':
            data = request.json
            command = "run " + data["command"]
            device = Device.devices[device_id]
            message = {"message":Command.Run(device, command)}
            return(jsonify(message))

##################GROUPS################################

    @flask_server.route('/groups', methods=["GET", "POST", "DELETE"])
    def HTTP_Groups():
        if request.method == "GET":
            groups = Command.Group_List()
            return(jsonify(groups))
        elif request.method == "POST":
            data = request.json
            group_name = data["group"]
            message = Command.Group_Create(group_name)
            return(jsonify(message))
        elif request.method == "DELETE":
            data = request.json
            group_name = data["group"]
            message = Command.Group_Delete(group_name)
            return(jsonify(message))

        



    @flask_server.route('/groups/<string:group_name>', methods=["GET", "DELETE", "POST"])
    def HTTP_Group(group_name):
        if request.method == 'GET':
            group = Command.Get_Group_By_Name(group_name)
            return(jsonify(group))
        if request.method == 'DELETE':
            data = request.json
            device = Device.devices[data['id']]
            group = Group.groups[group_name]
            message = Command.Group_Remove(group, device)
            return(jsonify(message))
        if request.method == 'POST':
            data = request.json
            device = Device.devices[data['id']]
            group = Group.groups[group_name]
            return(jsonify(Command.Group_Add(group,device)))


