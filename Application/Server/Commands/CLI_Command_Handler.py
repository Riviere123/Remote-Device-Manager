from Commands.Commands import Command
from Commands.Command_Handler import Command_Handler
from Device import Device, Group

class CLI_Command_Handler():
    def Client_Command(client_device, data):                                #Calls the command if a command is found in the data
        split_data = data.lower().split(" ")
        length, command = Command_Handler.Check_For_Client_Command(split_data)
        arguments = [client_device] + split_data[length:]                     
        if command != None:
            print(Command_Handler.Process_Command(command, arguments))
        else:
            print(f"{client_device.name}: {data}")                              #if no command was found print the data to the server console

    def Server_Command():                                                       #This is our servers terminal and will find and execute commands from user input
        data_input = input("\n")
        split_data = data_input.lower().split(" ")
        length, command = Command_Handler.Check_For_Server_Command(split_data)                                                                                      
        arguments = split_data[length:]

        if command != None:
            print(Command_Handler.Process_Command(command, arguments))


