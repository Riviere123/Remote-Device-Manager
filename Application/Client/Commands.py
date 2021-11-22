from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
import os

#Sends the message to the server
class Command():
    def Send(message):       
        Protocol_Send(Device.this_device.server, message)

    #Sets our device name locally and on the server
    def Set_Name(name):      
        Device.this_device.name = name
        Protocol_Send(Device.this_device.server, f"set name {name}" )

    #Sets the device type locally and on the server
    def Set_Type(archetype): 
        Device.this_device.archetype = archetype
        Protocol_Send(Device.this_device.server, f"set type {archetype}")

    #Get info about this device
    def Self():              
        return Device.this_device

    #Run a terminal command on this device
    #TODO pipe error message to the server
    def Run_Command(data, from_server):
        stream = os.popen(data)
        output = stream.read()
        if from_server:                                        #If the command was from the server send the output to the server
            Protocol_Send(Device.this_device.server, output)
            return(f"{data} called from Server")
        else:                                                  #otherwise just print to the console
            return output

class Command_Handler():
    def Check_For_Command(split_data):              #Checks for a command in the given list of strings
        commands = {'set name':Command.Set_Name, "set type":Command.Set_Type, 'self':Command.Self, 'run':Command.Run_Command}
        for i in range(4,0,-1):                     #Check from longest command to shortest command.
            command = " ".join(split_data[0:i])
            if command in commands.keys():
                return commands[command]



class CLI_Command_Handler():
    def Terminal_Command(data_input, from_Server):  #Takes a data input and if the data is from the server.
        split_data = data_input.lower().split(" ")  #Split the data
        command = Command_Handler.Check_For_Command(split_data)     #Check the data for any commands
        if command == Command.Set_Name:
            name = split_data[2]
            command(name)
        elif command == Command.Set_Type:
            archetype = split_data[2]
            command(archetype)
        elif command == Command.Self:
            print(command())
        elif command == Command.Run_Command:
            data = " ".join(split_data[1:])
            print(command(data, from_Server))
        else:                                        #If no command is found
            if from_Server:                          #If the data was from the server
                print(f"Server: {data_input}")       #Print the message from the server
            else:                                    #If the data was from the client
                Command.Send(data_input)                     #send the message to the server

