from enum import Enum

class Connection_State(Enum):
    connecting = 0
    connected = 1
    disconnected = 2

class Client():
    clients = []
    def __init__(self, connection):
        self.connection = connection
        Client.clients.append(self)
    
    def disconnect(self):
        if self.connection != None:
            self.connection.close()
            self.connection = None
            self.connection_state = Connection_State.disconnected
    
    def connect(self, connection):
        self.connection = connection
        self.connection_state = Connection_State.connected