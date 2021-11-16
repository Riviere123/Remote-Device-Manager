from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send

################## Commands called from a client ############################
def Set_Name(client_device, split_data):
    name = split_data[2]
    if name in Device.devices.keys():
        Protocol_Send(client_device.client, "Error: That name is already in use.")
        print("Error: Device name is already in use.")
    else:
        new_name = name                                              
        print(f"{client_device.name}'s name has been changed to {new_name}")
        client_device.Change_Name(new_name)
def Set_Type(client_device, split_data):
    new_type = split_data[2]                                               
    print(f"{client_device.name}'s device type changed to {new_type}")
    client_device.archetype = new_type

################## Commands called from server ############################
def Send(split_data):
    try:
        Protocol_Send(Device.devices[split_data[1]].client, " ".join(split_data[2:]))
        print(f"Message successfully sent to {Device.devices[split_data[1]].name}")
    except:
        print("Error: Client doesn't exist by that name. Or you're trying to send unsuported data values.")
def List():
    [print(f"Name:{Device.devices[i].name} Type:{Device.devices[i].archetype}") for i in Device.devices.keys()]

def Run(split_data):
    try:
        formatted = " ".join(split_data[0:1] + split_data[2:])
        print(formatted)
        Protocol_Send(Device.devices[split_data[1]].client,formatted)
    except:
        print("Error: Client doesn't exist by that name. Or you're trying to send unsuported data values.")
def Group_Create(split_data):
    group_name = split_data[2]
    if group_name in Group.groups.keys():
        print(f"Group {group_name} already exists.")
    else:
        Group(group_name)
        print(f"Group {group_name} created")
def Group_Add(split_data):
    group_name = split_data[2]
    device_name = split_data[3]
    try:
        group = Group.groups[group_name]
        device = Device.devices[device_name]
        if device in group.devices:
            print("Device already exists in that group.")
        else:
            group.Add_Device(device)
            device.group = group
            print(f"Added {device_name} to {group_name}")
    except Exception as e:
        print(e)
def Group_List():
    print(Group.groups)
def Group_Delete(split_data):
    try:
        group_name = split_data[2]
        Group.Group_Delete(group_name)
        print(f"{group_name} deleted")
    except Exception as e:
        print(e)
def Group_Remove(split_data):
    try:
        group_name = split_data[2]
        group = Group.groups[group_name]
        device_name = split_data[3]
        device = Device.devices[device_name]
        group.Remove_Device(device)
        print(f"{device_name} removed from {group_name}")
    except Exception as e:
        print(e)
def Group_Send(split_data):
    try:
        group_name = split_data[2]
        group = Group.groups[group_name]
        message = " ".join(split_data[3:])
        for device in group.devices:
            Protocol_Send(device.client, message)
    except Exception as e:
        print(e)