from Commands import *

commands = ['set name', 'set type', "self", "run"]
def Check_For_Command(split_data): #Checks for commands in a list of strings
    for i in range(4,0,-1):
        command = " ".join(split_data[0:i])
        if command in commands:
            return command

def Terminal_Command(data_input, from_Server): #Runs commands that are found if none are found send the data to the server.
    split_data = data_input.lower().split(" ")
    command = Check_For_Command(split_data)
    if command in commands:
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
    else:
        if from_Server:
            print(data_input)
        else:
            Send(f"Server: {data_input}")
