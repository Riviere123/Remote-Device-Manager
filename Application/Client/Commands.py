from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
# import os
from subprocess import PIPE, Popen

#Sends the message to the server
class Command():
    def Send(message):       
        Protocol_Send(Device.this_device.server, message)

    #Sets our device name locally and on the server
    def Set_Name(name, from_server):      
        Device.this_device.name = name
        if not from_server:
            Protocol_Send(Device.this_device.server, f"set name {name}" )

    #Sets the device type locally and on the server
    def Set_Type(archetype, from_server): 
        Device.this_device.archetype = archetype
        if not from_server:
            Protocol_Send(Device.this_device.server, f"set type {archetype}")
    
    def Set_Id(id, from_server):
        if from_server:
            Device.this_device.id = id

    #Get info about this device
    def Self():              
        return Device.this_device

    #Run a terminal command on this device
    def Run_Command(data, from_server):
        try:
            p = Popen(data, shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            payload = f"#|#stdout {stdout.decode()} #|#stderr {stderr.decode()}"
            if from_server:
                Protocol_Send(Device.this_device.server,"run output " + payload)
                return(f"{data} called from Server")
            else:
                return payload
        except Exception as e:
            print(e)

class Command_Handler():
    def Check_For_Command(split_data):              #Checks for a command in the given list of strings
        commands = {'set id':Command.Set_Id,'set name':Command.Set_Name, "set type":Command.Set_Type, 'self':Command.Self, 'run':Command.Run_Command}
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
            command(name, from_Server)
        elif command == Command.Set_Type:
            archetype = split_data[2]
            command(archetype, from_Server)
        elif command == Command.Self:
            print(command())
        elif command == Command.Run_Command:
            data = " ".join(split_data[1:])
            print(command(data, from_Server))
        elif command == Command.Set_Id:
            command(split_data[2], from_Server)
        else:                                        #If no command is found
            if from_Server:                          #If the data was from the server
                print(f"Server: {data_input}")       #Print the message from the server
            else:                                    #If the data was from the client
                Command.Send(data_input)                     #send the message to the server

