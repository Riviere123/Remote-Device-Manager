from Commands.Commands import Command
from Commands.Command_Handler import Command_Handler
from Device import Device, Group

class CLI_Command_Handler():
    def Client_Command(client_device, data):                                #Calls the command if a command is found in the data
        split_data = data.lower().split(" ")
        command = Command_Handler.Check_For_Client_Command(split_data)                      
        if command:
            print(f"{command.__name__} called from {client_device.name}")
            if command == Command.Set_Name:
                name = split_data[2]
                print(Command.Set_Name(client_device, name))                           
            elif command == Command.Set_Type:
                new_type = split_data[2]     
                print(Command.Set_Type(client_device, new_type))
        else:
            print(f"{client_device.name}: {data}")                              #if no command was found print the data to the server console

    def Server_Command():                                                       #This is our servers terminal and will find and execute commands from user input
        data_input = input("\n")
        split_data = data_input.lower().split(" ")
        command = Command_Handler.Check_For_Server_Command(split_data)                                                                                      

        if command == Command.Send:
            try:
                device = Device.devices[split_data[1]]
                message = " ".join(split_data[2:])
                print(command(device, message))
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Send (Device id) (Message). ")
        elif command == Command.List:
            try:
                print(command())
            except Exception as e:
                print(e)
        elif command == Command.Run:
            try:
                run_command = " ".join(split_data[0:1] + split_data[2:])
                device = Device.devices[split_data[1]]
                command(device, run_command)
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Run (Device id) (Terminal Command).")

        elif command == Command.Delete:
            try:
                device = Device.devices[split_data[1]]
                print(command(device))
            except Exception as e:
                print(f"Error: {e} The device ID was not found or the format was not correct.\nCorrect format Delete (Device id).")

        elif command == Command.Group_Create:
            try:
                group_name = split_data[2]
                print(command(group_name))
            except Exception as e:
                print(f"Error: {e}.\nCorrect format Group Create (Group Name).")

        elif command == Command.Group_Add:
            try:
                group_name = split_data[2]
                device_name = split_data[3]
                group = Group.groups[group_name]
                device = Device.devices[device_name]
                print(command(group, device))
            except Exception as e:
                print(f"Error: {e} The device ID was not found, the group was not found, or the format was not correct.\nCorrect format Group Add (Group Name) (Device id).")

        elif command == Command.Group_List:
            try:
                print(command())
            except Exception as e:
                print(f"Error: {e}.\nCorrect format Group List or Group ls.")
        elif command == Command.Group_Delete:
            try:
                group_name = split_data[2]
                print(command(group_name))
            except Exception as e:
                print(e)
        elif command == Command.Group_Remove:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                device_name = split_data[3]
                device = Device.devices[device_name]
                print(command(group, device))
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Remove (Group) (Device id).")
        elif command == Command.Group_Send:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                message = " ".join(split_data[3:])
                print(command(group, message))
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Send (Group) (Message).")

        elif command == Command.Group_Run:
            try:
                group_name = split_data[2]
                group = Group.groups[group_name]
                run_command = "run " + " ".join(split_data[3:])
                command(group, run_command)
            except Exception as e:
                print(f"Error: {e} The device id was not found or the group name was not found.\nCorrect format Group Run (Group) (Terminal Command).")


