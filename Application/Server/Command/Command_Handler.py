from Command.Commands import *
from Device import Device, Group
import sys, os

###COMMANDS SUMMARY###
#NOTE: To add new commands first -> Create Command function inside Commands.py -> Add the command to the
#      client_commands or server_commands dictionary depending on who you want
#      to be able to call the command. -> Finally add the command to the Process_Command function

###client_commands### commands called from the client
# set name (name) - sets the devices name on the server
# set type (type) - sets the devices archetype on the server
# run output (data) - delivers the run commands output and stores it on that device object
# attach mod (data) - sends module/sensor information to the server and attaches those modules to the device
# set frame (frame) - sets the current camera frame on the module of the device object

###server_commands### commands called from the server
# send (device_id) - sends the message to the device 
# list|ls - lists all connected devices and displays their information
# run (device_id) (terminal_command) - runs the terminal command on the device and recieve the stdout and stderr of the command
# delete (device_id) - deletes the device object and disconnects the device from the server
# group create (group_name) - creates a group of group_name
# group list|ls - lists all the groups and the devices within those groups
# group add (group_name) (device_id) - adds the device_id to the group_name
# group delete (group_name) - deletes the group with the given name
# group remove (group_name) (device_id) - removes the device_id from the group_name
# group send (group_name) - sends a message to every device in the group
# group run (group_name) (terminal_command) - runs the terminal command on every device in the group and returns the output of everyone.

client_commands={         #Dictionary of what the client can send to the server and the corresponding commands it calls.                                                                                                
    "set name":Set_Name, "set type":Set_Type, "run output":Run_Output, "attach mod":Attach_Module, "set frame":Set_Frame
    }
server_commands={         #Dictionary of what the server can enter in the terminal and what command it corresponds to.
    "send":Send, "list":List, "ls":List, "run":Run, "delete":Delete,
    "group create":Group_Create, "group list":Group_List, "group ls":Group_List, "group add":Group_Add,
    "group delete":Group_Delete, "group remove":Group_Remove, "group send":Group_Send, "group run": Group_Run, 
    }

#TODO: Can probably merge the to check_for_commands into one and pass in if the client or server is calling it instead.

def Check_For_Client_Command(split_data):                   #Checks for a command against the client_commands in the given list of strings
    for i in range(0,4):
        command = " ".join(split_data[0:i]).lower()
        if command in client_commands.keys():
            return (i,client_commands[command])
    return (None,None)
    
def Check_For_Server_Command(split_data):                   #Checks for a command against the server_commands in the given list of strings
    for i in range(4,0,-1):
        command = " ".join(split_data[0:i]).lower()
        if command in server_commands.keys():
            return (i,server_commands[command])
    return (None,None)

def Process_Command(called_command, arguments):            #When we process the command we pass the command itself and the arguments
    if called_command == Send:                             #Based on the command given format the arguments to fit the command needs
        try:                                               #This is where failed commands get caught and we return the error
            device = Device.devices[arguments[0]]
            message = " ".join(arguments[1:])
            return(called_command(device, message))
        except Exception as e:
            return ({"error": f"{e} The device ID was not found or the format was not correct. Correct format Send (Device id) (Message)."})

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
            return({"error": f"{e} The device ID was not found or the format was not correct. Correct format Run (Device id) (Terminal Command)."})

    elif called_command == Delete:
        try:
            device = Device.devices[arguments[0]]
            return(called_command(device))
        except Exception as e:
            return({"error": f"{e} The device ID was not found or the format was not correct. Correct format Delete (Device id)."})

    elif called_command == Group_Create:
        try:
            group_name = arguments[0]
            if " " in group_name:
                return({"error": "Group name cannot contain a space."})
            return(called_command(group_name))
        except Exception as e:
            return({"error": f"{e}. Correct format Group Create (Group Name)."})

    elif called_command == Group_Add:
        try:
            group_name = arguments[0]
            device_id = arguments[1]
            group = Group.groups[group_name]
            device = Device.devices[device_id]
            return(called_command(group,device))
        except Exception as e:
            return({"error": f"{e} The device ID was not found, the group was not found, or the format was not correct. Correct format Group Add (Group Name) (Device id)."})
    
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
            return({"error": f"{e} The device id was not found or the group name was not found. Correct format Group Remove (Group) (Device id)."})
    
    elif called_command == Group_Send:
        try:
            group_name = arguments[0]
            group = Group.groups[group_name]
            message = " ".join(arguments[1:])
            return(called_command(group, message))
        except Exception as e:
            return({"error": f"{e} The device id was not found or the group name was not found. Correct format Group Send (Group) (Message)."})
    
    elif called_command == Group_Run:
        try:
            group_name = arguments[0]
            group = Group.groups[group_name]
            run_command = " ".join(["run"] + arguments[1:])
            return(called_command(group, run_command))   
        except Exception as e:
            return({"error": f"{e} The group name was not found. Correct format Group Run (Group) (Terminal Command)."})
    
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
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return({"error": f"{e} Invalid device id."})
    
    elif called_command == Run_Output:
        try:
            device = Device.devices[arguments[0]]
            arguments = " ".join(arguments[1:])
            return called_command(device, arguments)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
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
    
    elif called_command == Attach_Module:
        try:
            device = arguments[0]
            return(called_command(device, arguments[1:]))
        except Exception as e:
            return({"error": "While recieving modular data"})
    
    elif called_command == Set_Frame:
        try:
            device = arguments[0]
            called_command(device, arguments[1:])
            # return(called_command(device, arguments[1:]))
        except Exception as e:
            return({"error": e})
        