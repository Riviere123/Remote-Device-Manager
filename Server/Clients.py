from enum import Enum
from datetime import datetime

class Connection_State(Enum):
    connecting = "connecting"
    connected = "connected"
    disconnected = "disconnected"

class Client():
    clients = []
    id_count = 0
    def __init__(self, connection, address, serial_number):
        self.connection_time = None
        self.disconnection_time = None
        self.address = address
        self.connection_state = Connection_State.connecting
        self.serial_number = serial_number
        self.id = self._setId()
        self.groups = []
        self.connect(connection, address)
        Client.clients.append(self)
    
    @staticmethod
    def clientSetup(connection, address, serial_number):
        for client in Client.clients:
            if client.serial_number == serial_number:
                client.connect(connection, address)
                return client
        new_client = Client(connection, address, serial_number)
        return new_client

    def _setId(self):
        Client.id_count+=1
        return Client.id_count


    def setDevice(self, device):
        self.device = device

    def disconnect(self):
        if self.connection != None:
            self.disconnection_time = datetime.now()
            self.connection.close()
            self.connection = None
            self.connection_state = Connection_State.disconnected
    
    def connect(self, connection, addr):
        self.connection_time = datetime.now()
        self.connection = connection
        self.address = addr
        self.connection_state = Connection_State.connected
    
    def __str__(self):
        string_groups = []
        for group in self.groups:
            string_groups.append(str(group))
        return(f"id:{self.id} ip:{self.address} groups:{string_groups} state:{self.connection_state.value}")
    
    