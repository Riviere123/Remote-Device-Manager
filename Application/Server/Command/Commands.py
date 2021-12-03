from Device import Device, Group
from DataFormatter import Protocol_Send
import time
################## Commands called from a client ############################
def Set_Name(device, new_name):
    device = Device.devices[device]         
    old_name = device.name                      
    device.Change_Name(new_name)
    Protocol_Send(device.client, "set name "+ new_name)
    return({"message": f"{old_name}'s name has been changed to {new_name}"})

def Set_Type(device, new_type): 
    device = Device.devices[device]                     
    device.Change_Type(new_type)
    Protocol_Send(device.client, "set type "+ new_type)
    return({"message": f"{device.name}'s device type changed to {new_type}"})

def Run_Output(device, output):
    device.run_command_output = output


################## Commands called from server ############################
def Send(device, message):
    if device.client != None:
        Protocol_Send(device.client, message)
        return({"message":"Message sent"})
    else:
        return({"error":f"{device} is not connected"}) 
#TODO Remove debug features that displays serial number
def List():
    payload = []
    for id in Device.devices.keys():
        device = Device.devices[id]
        connected = "Connected"
        group_names = []
        if device.client == None:
            connected = "Disconnected"
        for group in device.groups:
            group_names.append(group.name)
        payload.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected, "groups":group_names, "serial": device.serial})
    return(payload)

def Delete(device):
    device.Delete_Device()
    return({"message":f"{device.name} was deleted."})

def Run(device, run_command):
    if device.client != None:
        Protocol_Send(device.client,run_command)
        timeout = 0
        message = {'message': 'Device not responding'}
        while device.run_command_output == None and timeout < 5:
            time.sleep(1)
            timeout += 1
        message = device.Get_Runcommand_Output()
    
    if message != None:
        split_data = message.split("#|#")
        payload = {}

        for x in split_data[1:]:
            payload[x[:6]] = x[6:]

        return(payload)
    else:
        return({"message":f"{device} is not connected"}) 

def Group_Create(group_name):
    group_name = group_name.lower() 
    if group_name in Group.groups.keys():
        return({"message":f"Group {group_name} already exists."})
    else:
        Group(group_name)
        return({"message":f"Group {group_name} created"})

def Group_Add(group, device):
    if device in group.devices:
        return({"message":"Device already exists in that group."})
    else:
        group.Add_Device(device)
        device.groups.append(group)
        return({'message':f"Added {device.name} to {group.name}"})

def Group_List():
    payload = {}
    for group in Group.groups:
        payload_devices = []
        for device in Group.groups[group].devices:
            connected = "Connected"
            if device.client == None:
                connected = "Disconnected"
            payload_devices.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
        payload[group] = payload_devices
    return (payload)

def Group_Delete(group_name):
    Group.Group_Delete(group_name)
    return({'message':f"{group_name} deleted"})

def Group_Remove(group, device):
    group.Remove_Device(device)
    device.groups.remove(group)
    return({'message':f"{device.name} removed from {group.name}"})

def Group_Send(group, message):
    for device in group.devices:
        Send(device, message)

def Group_Run(group, run_command):
    messages = {}
    for device in group.devices:
        messages[device.id] = Run(device,run_command)
    return(messages)

#################### API Specific commands #######################
def Get_Device_By_ID(id):
    device = Device.devices[id]
    connected = "Connected"
    if device.client == None:
        connected = "Disconnected"
    return({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})

def Get_Group_By_Name(group_name):
    group = Group.groups[group_name.lower()]
    payload_devices = []
    for device in group.devices:
        connected = "Connected"
        if device.client == None:
            connected = "Disconnected"
        payload_devices.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
    return(payload_devices)
