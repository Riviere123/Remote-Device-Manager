from Command.Commands import *

def Check_For_Command(split_data):              #Checks for a command in the given list of strings
    commands = {'set id':Set_Id,'set name':Set_Name, 
    "set type":Set_Type, 'self':Self, 'run':Run_Command}
    for i in range(4,0,-1):                     #Check from longest command to shortest 
        command = " ".join(split_data[0:i])
        if command in commands.keys():
            return (i,commands[command])
    return(None, None)

def Process_Command(command, arguments, from_server):
        if command == Set_Name:
            name = arguments[0]
            return(command(name, from_server))
        elif command == Set_Type:
            archetype = arguments[0]
            return(command(archetype, from_server))
        elif command == Self:
            return(command())
        elif command == Run_Command:
            data = " ".join(arguments[0:])
            return(command(data, from_server))
        elif command == Set_Id:
            return(command(arguments[0], from_server))

def Client_Terminal():
    while True:                                                                                                                                                      
        try:
            data_input = input("\n")                                                #Terminal input
            split_data = data_input.lower().split(" ")                              #Split the data
            length, command = Check_For_Command(split_data)  #Returns length(The index where the command ends) and the command that was found                                                                    
            arguments = split_data[length:]                                         #Designates what part of the split data is the arguments based on the index of the commands ending
            if command != None:                                                     #If there was a command found
                print(Process_Command(command, arguments, False))          #Process the command
            else:
                Send(data_input)
        except Exception as e:
            print(e)

def Server_Data_Processor(data):
    split_data = data.lower().split(" ")
    length, command = Check_For_Command(split_data)
    arguments = split_data[length:]
    if command != None:
        Process_Command(command, arguments, True)
    else:
        print(f"Server: {data}")