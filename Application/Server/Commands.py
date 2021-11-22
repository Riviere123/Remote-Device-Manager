from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send
class Command():
################## Commands called from a client ############################
    def Set_Name(device, new_name):
        if new_name in Device.devices.keys():
            Protocol_Send(device.client, "Error: That name is already in use.")
            return("Error: Device name is already in use.")
        else:                                            
            device.Change_Name(new_name)
            return(f"{device.name}'s name has been changed to {new_name}")  
    def Set_Type(device, new_type):                      
        device.Change_Type(new_type)
        return(f"{device.name}'s device type changed to {new_type}")

################## Commands called from server ############################
    def Send(device, message):
        if device.client != None:
            Protocol_Send(device.client, message)
            return("Message sent")
        else:
            return(f"{device} is not connected") 
    def List():
        return(Device.devices)
    def Delete(device):
        device.Delete_Device()
    def Run(device, run_command):
        if device.client != None:
            Protocol_Send(device.client,run_command)
        else:
            return(f"{device} is not connected") 
    def Group_Create(group_name): 
        if group_name in Group.groups.keys():
            return(f"Group {group_name} already exists.")
        else:
            Group(group_name)
            return(f"Group {group_name} created")
    def Group_Add(group, device):
        if device in group.devices:
            return("Device already exists in that group.")
        else:
            group.Add_Device(device)
            device.groups.append(group)
            return(f"Added {device.name} to {group.name}")
    def Group_List():
        return (Group.groups)
    def Group_Delete(group_name):
        Group.Group_Delete(group_name)
        return(f"{group_name} deleted")
    def Group_Remove(group, device):
        group.Remove_Device(device)
        device.groups.remove(group)
        return(f"{device.name} removed from {group.name}")
    def Group_Send(group, message):
        for device in group.devices:
            Command.Send(device, message)
    def Group_Run(group, run_command):
        for device in group.devices:
            Command.Run(device,run_command)
        
class Command_Handler():
    client_commands={
        "set name":Command.Set_Name, "set type":Command.Set_Type
        }
    server_commands={
        "send":Command.Send, "list":Command.List, "ls":Command.List, "run":Command.Run, "delete":Command.Delete,
        "group create":Command.Group_Create, "group list":Command.Group_List, "group ls":Command.Group_List, "group add":Command.Group_Add,
        "group delete":Command.Group_Delete, "group remove":Command.Group_Remove, "group send":Command.Group_Send, "group run": Command.Group_Run
        }
    def Check_For_Client_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(0,4):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.client_commands.keys():
                return Command_Handler.client_commands[command]

    def Check_For_Server_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(4,0,-1):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.server_commands.keys():
                return Command_Handler.server_commands[command]

class CLI_Command_Handler():
    def Client_Command(client_device, data):                                #Calls the command if a command is found in the data
        split_data = data.lower().split(" ")
        command = Command_Handler.Check_For_Client_Command(split_data)                      
        if command:
            print(f"{command.__name__} called from {client_device.name}")
            if command == Command.Set_Name:
                name = split_data[2]
                print(Command.Set_Name(client_device, name))                           
            elif command == Command.Set_Type:
                new_type = split_data[2]     
                print(Command.Set_Type(client_device, new_type))
        else:
            print(f"{client_device.name}: {data}")                              #if no command was found print the data to the server console

    def Server_Command():                                                       #This is our servers terminal and will find and execute commands from user input
        data_input = input("\n")
        split_data = data_input.lower().split(" ")
        command = Command_Handler.Check_For_Server_Command(split_data)                                                                                      

        if command == Command.Send:
            try:
                device = Device.devices[split_data[1]]
                message = " ".join(split_data[2:])
                print(command(device, message))
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Send (Device id) (Message). ")
        elif command == Command.List:
            try:
                print(command())
            except Exception as e:
                print(e)
        elif command == Command.Run:
            try:
                run_command = " ".join(split_data[0:1] + split_data[2:])
                device = Device.devices[split_data[1]]
                command(device, run_command)
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Run (Device id) (Terminal Command).")

        elif command == Command.Delete:
            try:
                device = Device.devices[split_data[1]]
                print(command(device))
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Delete (Device id).")

        elif command == Command.Group_Create:
            try:
                group_name = split_data[2]
                print(command(group_name))
            except Exception as e:
                print(f"Error: {e}.\nCorrect format Group Create (Group Name).")

        elif command == Command.Group_Add:
            try:
                group_name = split_data[2]
                device_name = split_data[3]
                group = Group.groups[group_name]
                device = Device.devices[device_name]
                print(command(group, device))
            except Exception as e:
                print(f"Error: {e} The device ID was not found, the group was not found, or the format was not correct.\nCorrect format Group Add (Group Name) (Device id).")

        elif command == Command.Group_List:
            try:
                print(command())
            except Exception as e:
                print(f"Error: {e}.\nCorrect format Group List or Group ls.")
        elif command == Command.Group_Delete:
            try:
                group_name = split_data[2]
                print(command(group_name))
            except Exception as e:
                print(e)
        elif command == Command.Group_Remove:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                device_name = split_data[3]
                device = Device.devices[device_name]
                print(command(group, device))
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Remove (Group) (Device id).")
        elif command == Command.Group_Send:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                message = " ".join(split_data[3:])
                print(command(group, message))
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Send (Group) (Message).")

        elif command == Command.Group_Run:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                run_command = "run " + " ".join(split_data[3:])
                command(group, run_command)
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Run (Group) (Terminal Command).")



