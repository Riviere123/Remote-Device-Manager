from Clients import Client
from Group import Group
from enum import Enum

class ResultType(Enum):
    Error = "Error"
    Success = "Success"

class CommandResult():
    def __init__(self, result_type, payload):
        """
        The object that gets returns after processing a command with process_command_request

        keyword arguments:
        result_type(enum(ResultType)) - distinguishes whether the command was successful or if there was an error.
        payload(string) - the string 
        """
        self.result_type = result_type
        self.payload = payload

class CommandRequest():
    def __init__(self, command_object, arguments):
        """
        packaged command request for the process_command_requests method to handle.

        keyword arguments:
        command_object(Command) - the referenced command object.
        arguments(list) - the list of arguments for the command.
        """
        self.command_object = command_object
        self.arguments = arguments

class Command():
    commands = []
    def __init__(self, command, help_message, description, string_shortcuts):
        """
        Initializes the command object

        Keyword arguments:
        command (method) - the command method you want this command to call.
        help_message (string) - When the first argument is help this string will be packaged as a CommandResult object
                       and returned.
        description (string) - When the list commands method is called, this is the message displayed to the user.
        string_shortcuts(list) - the shortcut for the CLI to be able to reference the command.
        """
        self.command = command
        self.help_message = help_message
        self.description = description
        self.string_shortcuts = string_shortcuts
        Command.commands.append(self)

    def process_command_request(command_request_object):
        """
        Processes the command request object passed which holds the command object and arguments.
        Keyword arguments:
        command_request_object(CommandRequest) - is the command request object which holds the command object and arguments to process.
        """
        cro = command_request_object
        if cro.arguments:
            if cro.arguments[0].lower() == "help":
                payload = cro.command.help_message
                result = CommandResult(ResultType.Success, payload)
                return result
        (result_type, payload) = cro.command_object.command(cro.arguments)
        result = CommandResult(result_type, payload)
        return result

    def _list_clients(arguments):
        payload = []
        for client in Client.clients:
            payload.append(str(client))
        payload = "\n".join(payload)
        result = ResultType.Success
        return (result, payload)
        

    def _list_commands(arguments):
        payload = []
        for command in Command.commands:
            payload.append(str(command))
        payload = "\n".join(payload)
        result = ResultType.Success
        return (result, payload)

    def _create_group(arguments):
        try:
            group = Group(arguments[0])
            payload = f"group {group.name} created."
            result = ResultType.Success
            return (result, payload)
        except:
            payload = "No group name specified."
            result = ResultType.Error
            return (result, payload)

    def _list_groups(arguments):
        payload = []
        for group in Group.groups:
            payload.append(str(group))
        payload = "\n".join(payload)
        result = ResultType.Success
        return (result, payload)
    
    def _get_group(arguments):
        try:
            for group in Group.groups:
                if group.name == arguments[0]:
                    clients = []
                    for client in group.clients:
                        clients.append(str(client))
                    clients = "\n".join(clients)
                    payload = (f"{clients}")
                    result = ResultType.Success
                    return (result, payload)
            payload = f"{arguments[0]} not found."
            result = ResultType.Error
            return (result, payload) 
        except:
            payload = "No group name specified."
            result = ResultType.Error
            return (result, payload)
    
    def _add_client_to_group(arguments):
        try:
            target_client = None
            target_group = None
            for client in Client.clients:
                if str(client.id) == arguments[1]:
                    target_client = client
                    break
            for group in Group.groups:
                if group.name == arguments[0]:
                    target_group = group
                    break

            if target_client == None:
                payload = "Client id not found."
                result = ResultType.Error
                return (result, payload)
            elif target_group == None:
                payload =  "Target group not found."
                result = ResultType.Error
                return (result, payload)
            if target_client in target_group.clients:
                payload = f"{target_client.id} is already in {target_group.name}."
                result = ResultType.Error
                return (result, payload)
            else:
                target_group.clients.append(target_client)
                target_client.groups.append(target_group)
                payload = f"Added {target_client.id} to {target_group.name}"
                result = ResultType.Success
                return (result, payload)
        except:
            payload = "malformed command."
            result = ResultType.Error
            return (result, payload)

    def _remove_client_from_group(arguments):
        try:
            target_client = None
            target_group = None
            for group in Group.groups:
                if group.name == arguments[0]:
                    target_group = group
                    break
            if target_group == None:
                payload =  "Target group not found."
                result = ResultType.Error
                return (result, payload)
            else:
                for client in target_group.clients:
                    if str(client.id) == arguments[1]:
                        target_client = client
                        break
            if target_client == None:
                payload = "That client was not found in this group."
                result = ResultType.Error
                return (result, payload)
            else:
                target_group.clients.remove(target_client)
                target_client.groups.remove(target_group)
                payload = f"removed {target_client.id} from {target_group.name}"
                result = ResultType.Success
                return (result, payload)

        except:
            payload = "malformed command."
            result = ResultType.Error
            return (result, payload)

    def _test(arguments):
        pass

    def __str__(self):
        return(self.description)

test = Command(Command._test, "format: test", "test: this is a test method", ["test"])
list_clients = Command(Command._list_clients, "format: ls | list", "ls | list: Lists all the clients that have connected to the server.", ["ls", "list"])
list_commands = Command(Command._list_commands, "format: commands", "commands: gets a list of all the commands and their descriptions", ["commands"])
create_group = Command(Command._create_group, "format: create group (group name)", "create group: creates a group to store clients and run group commands with.", ["create group"])
list_groups = Command(Command._list_groups, "format: lsg | list groups", "lsg | list groups: lists all created groups.", ["lsg", "list groups"])
get_group = Command(Command._get_group, "format: gg (group name) | get group (group name)", "gg | get group: lists all the clients in the given group.", ['gg', 'get group'])
add_client_to_group = Command(Command._add_client_to_group, "format: ag (group name) (client id)| add group (group name) (client id)", "ag | add group: Adds the client to the group.", ["ag", "add group"])
remove_client_from_group = Command(Command._remove_client_from_group, "format: remove (group name) (client id)", "remove: removes the client from the group.", ["remove"])

class Parser():
    def parse(data):
        pass

class CLIParser(Parser):
    def parse(data):
        """
        parses a string and pulls out the command and arguments. Packages the command and arguments into a 
        CommandRequest object and calls the process_command_request method which returns a CommandResult object.
        
        Keyword arguments:
        data(string) - a string of data to parse
        """
        _split_data = data.split()
        for i in range(4,0,-1):
            _string_command = " ".join(_split_data[0:i])
            for _command in Command.commands:
                for _string_shortcut in _command.string_shortcuts:
                    if _string_command.lower() == _string_shortcut.lower():
                        _arguments = _split_data[i:]
                        _command_request = CommandRequest(_command, _arguments)
                        _command_result = Command.process_command_request(_command_request)
                        return _command_result
        _command_result = CommandResult(ResultType.Error, "Invalid Command.")
        return _command_result