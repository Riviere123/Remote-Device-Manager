from Command.Commands import *

###COMMANDS SUMMARY###
#NOTE: To add new commands first -> Create Command function inside Commands.py -> Add the command to the
#      Check_For_Command dictionary below -> Finally add the command to the Process_Command function.
#set id - Used to set the client side id and is called from the server(NOTE: This only works from the server)
#set name - Sets the name of the client device. If called from client it will also send updated name info to the server.
#set type - Sets the archetype of the client device. If called from client it will also send updated name info to the server.
#self - returns the devices information
#run - Runs any terminal commands given and returns it's STDOUT and STDIN
#send mod - Sends all module data to the server (NOTE: A module is a device attachment IE. Camera/Sensors)
#start camera - Starts the camera stream by sending camera frames to the server (NOTE: endpoint is /devices/<string:device_id>/camera)
#stop camera - Stops the camera stream

def Check_For_Command(split_data):              #Checks for a command in the given list of strings
    commands = {'set id':Set_Id,'set name':Set_Name, 
    "set type":Set_Type, 'self':Self, 'run':Run_Command, 'send mod':Send_Mod_Data,
    'start camera':Start_Camera, 'stop camera':Stop_Camera}

    for i in range(4,0,-1):                     #Check from longest command to shortest so no commands are skipped(NOTE: Supports commands up to 4 words currently)
        command = " ".join(split_data[0:i])
        if command in commands.keys():
            return (i,commands[command])
    return(None, None)

def Process_Command(command, arguments, from_server):  #Processes the command and returns the result of the command
        if command == Set_Name:                        #Formats the arguments so each command is passed the correct and expected information
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
        elif command == Send_Mod_Data:
            return(command())
        elif command == Start_Camera:
            return(command())
        elif command == Stop_Camera:
            return(command())

def Client_Terminal():                                                              #The terminal for the client to enter commands
    while True:                                                                                                                                                      
        try:
            data_input = input("\n")                                                #Terminal input
            split_data = data_input.lower().split(" ")                              #Split the data
            length, command = Check_For_Command(split_data)                         #Returns length(The index where the command ends) and the command that was found                                                                    
            arguments = split_data[length:]                                         #Designates what part of the split data is the arguments based on the index of the commands ending
            if command != None:                                                     #If there was a command found
                output = Process_Command(command, arguments, False)                 
                if output != None:                                                  #Prevents printing None messages
                    print(output)                                                   #Process the command
            else:
                Send(data_input)                                                    #Send the message to the server if it was not a command
        except Exception as e:
            print(e)

def Server_Data_Processor(data):                                                    #Takes in data from the server and checks it for commands
    split_data = data.lower().split(" ")                                            #Split the data to work with it
    length, command = Check_For_Command(split_data)                                 #Checks for commands
    arguments = split_data[length:]                                                 #Arguments are everything after the command
    if command != None:                                                             #If a command is found, Process it.
        Process_Command(command, arguments, True)
    else:                                                                           #If no command was found then just print to terminal
        print(f"Server: {data}")