from Commands import *

commands = ['set name', 'set type', "self", "run"]
def Check_For_Command(split_data):              #Checks for a command in the given list of strings
    for i in range(4,0,-1):                     #Check from longest command to shortest command.
        command = " ".join(split_data[0:i])
        if command in commands:
            return command

def Terminal_Command(data_input, from_Server):  #Takes a data input and if the data is from the server.
    split_data = data_input.lower().split(" ")  #Split the data
    command = Check_For_Command(split_data)     #Check the data for any commands
    if command in commands:                     #If a command is found perform the command
        if command == 'set name':
            name = split_data[2]
            Set_Name(name)
        elif command == 'set type':
            archetype = split_data[2]
            Set_Type(archetype)
        elif command == 'self':
            Self()
        elif command == 'run':
            data = " ".join(split_data[1:])
            Run_Command(data, from_Server)
    else:                                        #If no command is found
        if from_Server:                          #If the data was from the server
            print(f"Server: {data_input}")       #Print the message from the server
        else:                                    #If the data was from the client
            Send(data_input)                     #send the message to the server
