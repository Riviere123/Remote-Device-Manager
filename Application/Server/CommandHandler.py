from Commands import *

################## Commands called from a client ############################

client_commands=[
    "set name", "set type"
    ]
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
            if command == "set name":
                Set_Name(client_device, split_data)                               #calls the change name method from the device
            elif command == "set type":
                Set_Type(client_device, split_data)                                    #Set archetype of the Device object of the client 
        else:
            print(f"{client_device.name}: {data}")                                    #For now just print the data strea
    except:
        print(f"{client_device.name}: {data}")                                        #For now just print the data stream


################## Commands called from server ############################


server_commands=[
    "send", "list", "ls", "run", 
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
        if command == "send":
            Send(split_data)
        elif command in ["list", "ls"]:
            List()
        elif command == "run":
            Run(split_data)
        elif command == "group create":
            Group_Create(split_data)
        elif command in ["group list", "group ls"]:
            Group_List()
        elif command == "group add":
            Group_Add(split_data)
        elif command == "group delete":
            Group_Delete(split_data)
        elif command == "group remove":
            Group_Remove(split_data)
        elif command == "group send":
            Group_Send(split_data)

