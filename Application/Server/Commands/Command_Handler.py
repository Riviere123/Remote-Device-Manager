from Commands.Commands import Command

class Command_Handler():
    client_commands={
        "set name":Command.Set_Name, "set type":Command.Set_Type
        }
    server_commands={
        "send":Command.Send, "list":Command.List, "ls":Command.List, "run":Command.Run, "delete":Command.Delete,
        "group create":Command.Group_Create, "group list":Command.Group_List, "group ls":Command.Group_List, "group add":Command.Group_Add,
        "group delete":Command.Group_Delete, "group remove":Command.Group_Remove, "group send":Command.Group_Send, "group run": Command.Group_Run
        }
    def Check_For_Client_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(0,4):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.client_commands.keys():
                return Command_Handler.client_commands[command]

    def Check_For_Server_Command(split_data):                               #Checks for a command in the given list of strings
        for i in range(4,0,-1):
            command = " ".join(split_data[0:i])
            if command in Command_Handler.server_commands.keys():
                return Command_Handler.server_commands[command]