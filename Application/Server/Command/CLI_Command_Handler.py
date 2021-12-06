from Command.Command_Handler import Process_Command, Check_For_Client_Command, Check_For_Server_Command


def Client_Command(client_device, data):                                     #Calls the command if a command is found in the data
    split_data = data.lower().split(" ")                                     #Splits the data into a list
    length, command = Check_For_Client_Command(split_data)   #Returns length(The index where the command ends) and the command that was found
    arguments = [client_device.id] + split_data[length:]                       #Add the client device to the beginning of the arguments
    if command != None:                                                      #If a command was found then process whatever command it was with the arguments
        print(Process_Command(command, arguments))
    else:
        print(f"{client_device.name}: {data}")                              #If no command was found print the data to the server console

def Server_Command():                                                       #This is our servers terminal and will find and execute commands from user input
    data_input = input("\n")                                                #Terminal input
    split_data = data_input.lower().split(" ")                              #Split the data
    length, command = Check_For_Server_Command(split_data)  #Returns length(The index where the command ends) and the command that was found                                                                    
    arguments = split_data[length:]                                         #Designates what part of the split data is the arguments based on the index of the commands ending

    if command != None:                                                     #If there was a command found
        print(Process_Command(command, arguments))          #Process the command


