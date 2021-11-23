from Commands.Commands import Command
from Device import Device, Group
class Command_Handler():
    client_commands={
        "set name":Command.Set_Name, "set type":Command.Set_Type
        }
    server_commands={
        "send":Command.Send, "list":Command.List, "ls":Command.List, "run":Command.Run, "delete":Command.Delete,
        "group create":Command.Group_Create, "group list":Command.Group_List, "group ls":Command.Group_List, "group add":Command.Group_Add,
        "group delete":Command.Group_Delete, "group remove":Command.Group_Remove, "group send":Command.Group_Send, "group run": Command.Group_Run, 
        }
    def Check_For_Client_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(0,4):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.client_commands.keys():
                return (i,Command_Handler.client_commands[command])
        return (None,None)
        
    def Check_For_Server_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(4,0,-1):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.server_commands.keys():
                return (i,Command_Handler.server_commands[command])
        return (None,None)

    def Process_Command(called_command, arguments):
        if called_command == Command.Send:
            try:
                device = Device.devices[arguments[0]]
                message = " ".join(arguments[1:])
                return(called_command(device, message))
            except Exception as e:
                return (f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Send (Device id) (Message). ")
        elif called_command == Command.List:
            try:
                return(called_command())
            except Exception as e:
                return(e)
        elif called_command == Command.Run:
            try:
                run_command = " ".join(["run"] + arguments[1:])
                device = Device.devices[arguments[0]]
                called_command(device, run_command)
            except Exception as e:
                return(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Run (Device id) (Terminal Command).")
        elif called_command == Command.Delete:
            try:
                device = Device.devices[arguments[0]]
                return(called_command(device))
            except Exception as e:
                return(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Delete (Device id).")
        elif called_command == Command.Group_Create:
            try:
                group_name = arguments[0]
                return(called_command(group_name))
            except Exception as e:
                return(f"Error: {e}.\nCorrect format Group Create (Group Name).")
        elif called_command == Command.Group_Add:
            try:
                group_name = arguments[0]
                device_name = arguments[1]
                group = Group.groups[group_name]
                device = Device.devices[device_name]
                return(called_command(group,device))
            except Exception as e:
                return(f"Error: {e} The device ID was not found, the group was not found, or the format was not correct.\nCorrect format Group Add (Group Name) (Device id).")
        elif called_command == Command.Group_List:
            try:
                return(called_command())
            except Exception as e:
                return(f"Error: {e}.\nCorrect format Group List or Group ls.")
        elif called_command == Command.Group_Delete:
            try:
                group_name = arguments[0]
                return(called_command(group_name))
            except Exception as e:
                return(e)
        elif called_command == Command.Group_Remove:
            try:
                group_name = arguments[0]
                group = Group.groups[group_name]
                device_name = arguments[1]
                device = Device.devices[device_name]
                return(called_command(group, device))
            except Exception as e:
                return(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Remove (Group) (Device id).")
        elif called_command == Command.Group_Send:
            try:
                group_name = arguments[0]
                group = Group.groups[group_name]
                message = " ".join(arguments[1:])
                return(called_command(group, message))
            except Exception as e:
                return(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Send (Group) (Message).")
        elif called_command == Command.Group_Run:
            try:
                group_name = arguments[0]
                group = Group.groups[group_name]
                run_command = " ".join(["run"] + arguments[1:])
                return(called_command(group, run_command))   
            except Exception as e:
                return(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Run (Group) (Terminal Command).")
        elif called_command == Command.Set_Type:
            try:
                device = arguments[0]
                type = arguments[1]
                return called_command(device, type)
            except Exception as e:
                return(e)
        elif called_command == Command.Set_Name:
            try:
                device = arguments[0]
                name = arguments[1]
                return called_command(device, name)
            except Exception as e:
                return(e)
