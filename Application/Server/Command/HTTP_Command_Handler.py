from Flask_Wrapper import flask_server, auth
from flask import jsonify, request, Response
from Command.Command_Handler import Process_Command
from Command.Commands import *
from Device import Device, Group
import cv2
#Home page#
@flask_server.route('/', methods=["GET"]) 
def Index():
    if request.method == 'GET':
        return(jsonify({"message":"Server is live! API docs at /swagger"}))

###################DEVICE#################################
@flask_server.route('/devices', methods=["GET"])
@auth.login_required
def HTTP_List_Devices():
    if request.method == 'GET':
        message = Process_Command(List, None)
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>', methods=["GET", "DELETE"])
@auth.login_required
def HTTP_Device(device_id):
    if request.method == 'GET':
        message = Process_Command(Get_Device_By_ID, [device_id])
        return(jsonify(message))
    elif request.method == 'DELETE':
        message = Process_Command(Delete, [device_id])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/name', methods=["POST"])
@auth.login_required
def HTTP_Device_Name(device_id):
    if request.method == 'POST':
        data = request.json
        name = data["name"]
        message = Process_Command(Set_Name, [device_id, name])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/type', methods=["POST"])
@auth.login_required
def HTTP_Device_Type(device_id):
    if request.method == 'POST':
        data = request.json
        new_type = data["type"]
        message = Process_Command(Set_Type,[device_id, new_type])
        return(jsonify(message))

@flask_server.route('/devices/<string:device_id>/run', methods=["POST"])
@auth.login_required
def HTTP_Device_Run(device_id):
    if request.method == 'POST':
        data = request.json
        command = data["command"]
        message = Process_Command(Run,[device_id, command])
        return(jsonify(message))

#TODO: Handle multiple cameras on one device
@flask_server.route('/devices/<string:device_id>/camera', methods=["GET"])
@auth.login_required
def HTTP_Device_Camera(device_id):
    if request.method == "GET":
        device = Device.devices[device_id]
        for module in device.modules:
            if module.archetype == "camera":            
                return Response(module.Start_Camera_Feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
        message = {"message": "No camera detected or the camera is not active."}
        return(jsonify(message))

##################GROUPS################################
@flask_server.route('/groups', methods=["GET", "POST", "DELETE"])
@auth.login_required
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
@auth.login_required
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
@auth.login_required
def HTTP_Group_Run(group_name):
    if request.method == 'POST':
        data = request.json
        command = data["command"]
        message = Process_Command(Group_Run,[group_name, command])
        return(jsonify(message))


