from Flask_Wrapper import flask_server
from flask import jsonify, request
from Command.Command_Handler import Process_Command
from Command.Commands import *
from Device import Device, Group

#TODO Wireshark the API calls

@flask_server.route('/', methods=["GET"])
def Index():
    if request.method == 'GET':
        return(jsonify({"message":"Server is live!"}))

###################DEVICE#################################
@flask_server.route('/devices', methods=["GET"])
def HTTP_List_Devices():
    if request.method == 'GET':
        message = Process_Command(List, None)
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>', methods=["GET", "DELETE"])
def HTTP_Device(device_id):
    if request.method == 'GET':
        message = Process_Command(Get_Device_By_ID, [device_id])
        return(jsonify(message))
    elif request.method == 'DELETE':
        message = Process_Command(Delete, [device_id])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/name', methods=["POST"])
def HTTP_Device_Name(device_id):
    if request.method == 'POST':
        data = request.json
        name = data["name"]
        device = Device.devices[device_id]
        message = Process_Command(Set_Name, [device, name])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/type', methods=["POST"])
def HTTP_Device_Type(device_id):
    if request.method == 'POST':
        data = request.json
        new_type = data["type"]
        device = Device.devices[device_id]
        message = Process_Command(Set_Type,[device, new_type])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/run', methods=["POST"])
def HTTP_Device_Run(device_id):
    if request.method == 'POST':
        data = request.json
        command = data["command"]
        message = Process_Command(Run[device_id, command])
        return(jsonify(message))

##################GROUPS################################

@flask_server.route('/groups', methods=["GET", "POST", "DELETE"])
def HTTP_Groups():
    if request.method == "GET":
        message = Process_Command(Group_List, None)
        return(jsonify(message))
    elif request.method == "POST":
        data = request.json
        group_name = data["group"]
        message = Process_Command(Group_Create, [group_name])
        return(jsonify(message))
    elif request.method == "DELETE":
        data = request.json
        group_name = data["group"]
        message = Process_Command(Group_Delete, [group_name])
        return(jsonify(message))

@flask_server.route('/groups/<string:group_name>', methods=["GET", "DELETE", "POST"])
def HTTP_Group(group_name):
    if request.method == 'GET':
        message = Process_Command(Get_Group_By_Name, [group_name])
        return(jsonify(message))
    if request.method == 'DELETE':
        data = request.json
        device = data['id']
        message = Process_Command(Group_Remove, [group_name, device])
        return(jsonify(message))
    if request.method == 'POST':
        data = request.json
        device = data['id']
        message = Process_Command(Group_Add, [group_name, device])
        return(jsonify(message))

@flask_server.route('/groups/<string:group_name>/run', methods=["POST"])
def HTTP_Group_Run(group_name):
    if request.method == 'POST':
        data = request.json
        command = data["command"]
        message = Process_Command(Group_Run,[group_name, command])
        return(jsonify(message))
