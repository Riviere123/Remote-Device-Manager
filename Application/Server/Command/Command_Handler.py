from Command.Commands import *
from Device import Device, Group


client_commands={         #Dictionary of what the client can send to the server and the corresponding commands it calls.                                                                                                
    "set name":Set_Name, "set type":Set_Type, "run output":Run_Output
    }
server_commands={         #Dictionary of what the server can enter in the terminal and what command it corresponds to.
    "send":Send, "list":List, "ls":List, "run":Run, "delete":Delete,
    "group create":Group_Create, "group list":Group_List, "group ls":Group_List, "group add":Group_Add,
    "group delete":Group_Delete, "group remove":Group_Remove, "group send":Group_Send, "group run": Group_Run, 
    }
def Check_For_Client_Command(split_data):                               #Checks for a command in the given list of strings
    for i in range(0,4):
        command = " ".join(split_data[0:i])
        if command in client_commands.keys():
            return (i,client_commands[command])
    return (None,None)
    
def Check_For_Server_Command(split_data):                               #Checks for a command in the given list of strings
    for i in range(4,0,-1):
        command = " ".join(split_data[0:i])
        if command in server_commands.keys():
            return (i,server_commands[command])
    return (None,None)

def Process_Command(called_command, arguments):                         #When we process the command we pass the command itself and the arguments
    if called_command == Send:                                  #Based on the command given format the arguments to fit the command needs
        try:                                                            #This is where failed commands get caught and we return the error
            device = Device.devices[arguments[0]]
            message = " ".join(arguments[1:])
            return(called_command(device, message))
        except Exception as e:
            return ({"error": f"{e} The device ID was not found or the format was not correct.\nCorrect format Send (Device id) (Message)."})

    elif called_command == List:
        try:
            return(called_command())
        except Exception as e:
            return({"error": e})

    elif called_command == Run:
        try:
            run_command = " ".join(["run"] + arguments[1:])
            device = Device.devices[arguments[0]]
            return(called_command(device, run_command))
        except Exception as e:
            return({"error": f"{e} The device ID was not found or the format was not correct.\nCorrect format Run (Device id) (Terminal Command)."})

    elif called_command == Delete:
        try:
            device = Device.devices[arguments[0]]
            return(called_command(device))
        except Exception as e:
            return({"error": f"{e} The device ID was not found or the format was not correct.\nCorrect format Delete (Device id)."})

    elif called_command == Group_Create:
        try:
            group_name = arguments[0]
            if " " in group_name:
                return({"error": "Group name cannot contain a space."})
            return(called_command(group_name))
        except Exception as e:
            return({"error": f"{e}.\nCorrect format Group Create (Group Name)."})

    elif called_command == Group_Add:
        try:
            group_name = arguments[0]
            device_id = arguments[1]
            group = Group.groups[group_name]
            device = Device.devices[device_id]
            return(called_command(group,device))
        except Exception as e:
            return({"error": f"{e} The device ID was not found, the group was not found, or the format was not correct.\nCorrect format Group Add (Group Name) (Device id)."})
    
    elif called_command == Group_List:
        try:
            return(called_command())
        except Exception as e:
            return({"error": f"{e}. Correct format Group List or Group ls."})
    
    elif called_command == Group_Delete:
        try:
            group_name = arguments[0]
            return(called_command(group_name))
        except Exception as e:
            return({"error": f"{e}the group name provided was not found."})
    
    elif called_command == Group_Remove:
        try:
            group_name = arguments[0]
            group = Group.groups[group_name]
            device_name = arguments[1]
            device = Device.devices[device_name]
            return(called_command(group, device))
        except Exception as e:
            return({"error": f"{e} The device id was not found or the group name was not found.\nCorrect format Group Remove (Group) (Device id)."})
    
    elif called_command == Group_Send:
        try:
            group_name = arguments[0]
            group = Group.groups[group_name]
            message = " ".join(arguments[1:])
            return(called_command(group, message))
        except Exception as e:
            return({"error": f"{e} The device id was not found or the group name was not found.\nCorrect format Group Send (Group) (Message)."})
    
    elif called_command == Group_Run:
        try:
            group_name = arguments[0]
            group = Group.groups[group_name]
            run_command = " ".join(["run"] + arguments[1:])
            return(called_command(group, run_command))   
        except Exception as e:
            return({"error": f"{e} The device id was not found or the group name was not found.\nCorrect format Group Run (Group) (Terminal Command)."})
    
    elif called_command == Set_Type:
        try:
            device = arguments[0]
            type = arguments[1]
            return called_command(device, type)
        except Exception as e:
            return({"error": f"{e} Invalid device id."})
    
    elif called_command == Set_Name:
        try:
            device = arguments[0]
            name = arguments[1]
            return called_command(device, name)
        except Exception as e:
            return({"error": f"{e} Invalid device id."})
    
    elif called_command == Run_Output:
        try:
            device = arguments[0]
            device.run_command_output = " ".join(arguments[1:])
        except Exception as e:
            return({"error": f"{e} Invalid device id."})

    elif called_command == Get_Device_By_ID:
        try:
            device = arguments[0]
            return(called_command(device))
        except Exception as e:
            return({"error": f"{e} Invalid device id."})
    
    elif called_command == Get_Group_By_Name:
        try:
            group = arguments[0]
            return(called_command(group))
        except Exception as e:
            return({"error": f"{e} Invalid group name."})