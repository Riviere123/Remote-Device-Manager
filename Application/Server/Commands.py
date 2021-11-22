from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send

#TODO Decouple command logic from how inputs and outputs are interpreted.

################## Commands called from a client ############################
def Set_Name(device, new_name):
    if new_name in Device.devices.keys():
        Protocol_Send(device.client, "Error: That name is already in use.")
        print("Error: Device name is already in use.")
    else:                                            
        print(f"{device.name}'s name has been changed to {new_name}")
        device.Change_Name(new_name)
def Set_Type(device, new_type):                       
    print(f"{device.name}'s device type changed to {new_type}")
    device.Change_Type(new_type)

################## Commands called from server ############################
def Send(device, message):
    if device.client != None:
        Protocol_Send(device.client, message)
    else:
        print(f"{device} is not connected")
        
def List():
    [print(f"{Device.devices[i]}") for i in Device.devices.keys()]

def Run(device, run_command):
    if device.client != None:
        Protocol_Send(device.client,run_command)
    else:
        print(f"{device} is not connected") 

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
        device.groups.append(group)
        print(f"Added {device.name} to {group.name}")

def Group_List():
    for group in Group.groups:
        print(f"{group} ##################################")
        for device in Group.groups[group].devices:
            print(device)

def Group_Delete(group_name):
        Group.Group_Delete(group_name)
        print(f"{group_name} deleted")

def Group_Remove(group, device):
    group.Remove_Device(device)
    device.groups.remove(group)
    print(f"{device.name} removed from {group.name}")

def Group_Send(group, message):
    for device in group.devices:
        Send(device, message)

def Group_Run(group, run_command):
    for device in group.devices:
        Run(device,run_command)
