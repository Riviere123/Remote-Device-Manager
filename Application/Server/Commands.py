from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send

################## Commands called from a client ############################
def Set_Name(device, new_name):
    if new_name in Device.devices.keys():
        Protocol_Send(device.client, "Error: That name is already in use.")
        print("Error: Device name is already in use.")
    else:                                            
        print(f"{device.name}'s name has been changed to {new_name}")
        device.Change_Name(new_name)
def Set_Type(client_device, new_type):                       
    print(f"{client_device.name}'s device type changed to {new_type}")
    client_device.archetype = new_type

################## Commands called from server ############################
def Send(device, message):
    Protocol_Send(device.client, message)
    print(f"Message successfully sent to {device.name}")
def List():
    [print(f"ID:{i} Name:{Device.devices[i].name} Type:{Device.devices[i].archetype}") for i in Device.devices.keys()]

def Run(device, run_command):
    print(run_command)
    Protocol_Send(device.client,run_command)
def Group_Create(group_name): 
    if group_name in Group.groups.keys():
        print(f"Group {group_name} already exists.")
    else:
        Group(group_name)
        print(f"Group {group_name} created")
def Group_Add(group, device):
    if device in group.devices:
        print("Device already exists in that group.")
    else:
        group.Add_Device(device)
        device.group = group
        print(f"Added {device.name} to {group.name}")
def Group_List():
    print(Group.groups)
def Group_Delete(group_name):
        Group.Group_Delete(group_name)
        print(f"{group_name} deleted")
def Group_Remove(group, device):
    group.Remove_Device(device)
    print(f"{device.name} removed from {group.name}")

def Group_Send(group, message):
    for device in group.devices:
        Protocol_Send(device.client, message)
def Group_Run(group, run_command):
    for device in group.devices:
        Protocol_Send(device.client,run_command)
