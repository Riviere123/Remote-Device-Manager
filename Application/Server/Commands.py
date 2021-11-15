from Device import Device
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
            if command == "set name":
                name = split_data[2]
                if name in Device.devices.keys():
                    Protocol_Send(client_device.client, "Error: That name is already in use.")
                    print("Error: Device name is already in use.")
                else:
                    new_name = name                                              #Take the third position as the new name
                    print(f"{client_device.name}'s name has been changed to {new_name}")
                    client_device.Change_Name(new_name)                                   #calls the change name method from the device
            elif command == "set type":
                new_type = split_data[2]                                              #Take the third position as the new name 
                print(f"{client_device.name}'s device type changed to {new_type}")
                client_device.archetype = new_type                                    #Set archetype of the Device object of the client 
        else:
            print(f"{client_device.name}: {data}")                               #For now just print the data stream

    except:
        print(f"{client_device.name}: {data}")                               #For now just print the data stream

###Commands sent to client
server_commands=["send", "list"]
def Check_For_Server_Command(split_data):
    for i in range(0,4):
        command = " ".join(split_data[0:i])
        if command in server_commands:
            return command

def Server_Command():
    data_input = input("")
    split_data = data_input.lower().split(" ")
    command = Check_For_Server_Command(split_data)
    if command in server_commands:                                                                                                   
        if command == "send":
            try:
                Protocol_Send(Device.devices[split_data[1]].client, " ".join(split_data[2:]))
                print(f"Message successfully sent to {Device.devices[split_data[1]].name}")
            except:
                print("Error: Client doesn't exist by that name. Or you're trying to send unsuported data values.")
        
        elif command == "list":
            [print(f"Name:{Device.devices[i].name} Type:{Device.devices[i].archetype}") for i in Device.devices.keys()]