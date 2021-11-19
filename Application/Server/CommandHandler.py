from Commands import *

################## Commands called from a client ############################
########### There are the commands that clients can call ####################
client_commands=[                                                       #The command names
    "set name", "set type"
    ]
    
def Check_For_Client_Command(split_data):                               #Checks for a command in the given list of strings
    for i in range(0,4):
        command = " ".join(split_data[0:i])
        if command in client_commands:
            return command

def Client_Command(client_device, data):                                #Calls the command if a command is found in the data
    split_data = data.lower().split(" ")
    command = Check_For_Client_Command(split_data)                      
    if command:
        print(f"{command} called from {client_device.name}")
        if command == "set name":
            name = split_data[2]
            Set_Name(client_device, name)                               
        elif command == "set type":
            new_type = split_data[2]     
            Set_Type(client_device, new_type)
    else:
        print(f"{client_device.name}: {data}")                              #if no command was found print the data to the server console


################## Commands called from server ############################
######Formats the data to fit the corresponding command then runs it#######

server_commands=[
    "send", "list", "ls", "run", "delete", 
    "group create", "group list", "group ls", "group add", "group delete", "group remove",
    "group send", "group run"
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
        if command == "send":
            try:
                device = Device.devices[split_data[1]]
                message = " ".join(split_data[2:])
                Send(device, message)
            except Exception as e:
                print(e)
        elif command in ["list", "ls"]:
            try:
                List()
            except Exception as e:
                print(e)
        elif command == "run":
            try:
                run_command = " ".join(split_data[0:1] + split_data[2:])
                device = Device.devices[split_data[1]]
                Run(device, run_command)
            except Exception as e:
                print(e)
        elif command == "delete":
            try:
                device = Device.devices[split_data[1]]
                print(device)
                device.Delete_Device()
            except Exception as e:
                print(e)
        elif command == "group create":
            try:
                group_name = split_data[2]
                Group_Create(group_name)
            except Exception as e:
                print(e)
        elif command == "group add":
            try:
                group_name = split_data[2]
                device_name = split_data[3]
                group = Group.groups[group_name]
                device = Device.devices[device_name]
                Group_Add(group, device)
            except Exception as e:
                print(e)
        elif command in ["group list", "group ls"]:
            try:
                Group_List()
            except Exception as e:
                print(e)
        elif command == "group delete":
            try:
                group_name = split_data[2]
                Group_Delete(group_name)
            except Exception as e:
                print(e)
        elif command == "group remove":
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                device_name = split_data[3]
                device = Device.devices[device_name]
                Group_Remove(group, device)
            except Exception as e:
                print(e)
        elif command == "group send":
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                message = " ".join(split_data[3:])
                Group_Send(group, message)
            except Exception as e:
                print(e)
        elif command == "group run":
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                run_command = "run " + " ".join(split_data[3:])
                Group_Run(group, run_command)
            except Exception as e:
                print(e)

