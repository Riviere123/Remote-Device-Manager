from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send

###Commands sent from client
client_commands=["set name", "set type"]
def Check_For_Client_Command(split_data):
    for i in range(0,4):
        command = " ".join(split_data[0:i])
        if command in client_commands:
            return command
def Client_Command(client_device, data):
    try:
        split_data = data.lower().split(" ")
        command = Check_For_Client_Command(split_data)
        if command:
            print(f"{command} called from {client_device.name}")
            ### set name
            if command == "set name":
                name = split_data[2]
                if name in Device.devices.keys():
                    Protocol_Send(client_device.client, "Error: That name is already in use.")
                    print("Error: Device name is already in use.")
                else:
                    new_name = name                                              
                    print(f"{client_device.name}'s name has been changed to {new_name}")
                    client_device.Change_Name(new_name)                               #calls the change name method from the device
            ### set type
            elif command == "set type":
                new_type = split_data[2]                                               
                print(f"{client_device.name}'s device type changed to {new_type}")
                client_device.archetype = new_type                                    #Set archetype of the Device object of the client 
        else:
            print(f"{client_device.name}: {data}")                                    #For now just print the data stream

    except:
        print(f"{client_device.name}: {data}")                                        #For now just print the data stream

###Commands sent to client
server_commands=["send", "list", "ls", "run", 
"group create", "group list", "group ls", "group add", "group delete", "group remove",
"group send"
]
def Check_For_Server_Command(split_data):
    for i in range(4,0,-1):
        command = " ".join(split_data[0:i])
        if command in server_commands:
            return command

def Server_Command():
    data_input = input("\n")
    split_data = data_input.lower().split(" ")
    command = Check_For_Server_Command(split_data)
    if command in server_commands:
        ### send                                                                                                   
        if command == "send":
            try:
                Protocol_Send(Device.devices[split_data[1]].client, " ".join(split_data[2:]))
                print(f"Message successfully sent to {Device.devices[split_data[1]].name}")
            except:
                print("Error: Client doesn't exist by that name. Or you're trying to send unsuported data values.")
        ### list
        elif command in ["list", "ls"]:
            [print(f"Name:{Device.devices[i].name} Type:{Device.devices[i].archetype}") for i in Device.devices.keys()]
        ### run
        elif command == "run":
            try:
                formatted = " ".join(split_data[0:1] + split_data[2:])
                print(formatted)
                Protocol_Send(Device.devices[split_data[1]].client,formatted)
            except:
                print("Error: Client doesn't exist by that name. Or you're trying to send unsuported data values.")
        ### group create
        elif command == "group create":
            group_name = split_data[2]
            if group_name in Group.groups.keys():
                print(f"{group_name} already exists.")
            else:
                Group(group_name)
                print(f"{group_name} created")
        ### group list
        elif command in ["group list", "group ls"]:
            print("listing group")
            print(Group.groups)
        ### group add
        elif command == "group add":
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
                    print(f"Added{device_name} to {group_name}")
            except Exception as e:
                print(e)
        ### group delete
        elif command == "group delete":
            try:
                group_name = split_data[2]
                Group.Group_Delete(group_name)
                print(f"{group_name} deleted")
            except Exception as e:
                print(e)
        ### group remove
        elif command == "group remove":
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                device_name = split_data[3]
                device = Device.devices[device_name]
                group.Remove_Device(device)
                print(f"{device_name} removed from {group_name}")
            except Exception as e:
                print(e)
        ### group send
        elif command == "group send":
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                message = " ".join(split_data[3:])
                for device in group.devices:
                    Protocol_Send(device.client, message)
            except Exception as e:
                print(e)

