from enum import Enum

def listClients(arguments):
    return("list of clients")

class Command():
    commands = {"ls":listClients}
    def __init__(self, command, arguments):
        self.command = command
        self.arguments = arguments
    
    def run(self):
        return(self.command(self.arguments))

    
class Formats(Enum):
    CLI = 0
    API = 1
    IOT = 2

class Parser():
    def __init__(self, data, format):
        self.format = format
        self.data = data
        self.command = None

    def parse(self):
        if self.format == Formats.CLI:
            split_data = self.data.lower().split()
            for i in range(4,0,-1):
                command = " ".join(split_data[0:i])
                if command in Command.commands.keys():
                    arguments = split_data[i:]
                    command = Command.commands[command]
                    self.command = Command(command, arguments)
                    break

    def runAndStyle(self):
        if self.format == Formats.CLI:
            if self.command != None:
                output = self.command.run()
            else:
                output = "No command found. Type commands for a list of commands."
            return output