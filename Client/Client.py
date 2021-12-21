import ssl, socket, threading, Config
from SerialGenerator import Handle_Serial
from Protocols import protocolReceive, protocolSend
from enum import Enum


class Connection_State(Enum):
    connecting = "connecting"
    connected = "connected"
    disconnected = "disconnected"

class Connection():
    connections = []
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.state = Connection_State.disconnected
        self.connection = None

    def handleConnection(self, connection):
        while True:                                   #If we have an active connection
            try:
                data = protocolReceive(connection)    #Recieve data from server
                #TODO: Server command handler
                print(data)
            except:                             
                self._disconnect()             
                break

    def connect(self):
        self.state = Connection_State.connecting
        certificate = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
        certificate.load_verify_locations('./Authentication/certificate.pem')                   #Load the cert so it will be accepted since it is self signed
        connection = certificate.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host)
        connection.connect((self.host, self.port))
        self.connection = connection
        self._sendSetupData()
        Connection.connections.append(connection)
        self.state = Connection_State.connected
        print(f"Connected to {self.host}:{self.port}")
        receive_thread = threading.Thread(target=self.handleConnection, args=(connection,))              #Create and start a thread to recieve data
        receive_thread.start()
    
    def _sendSetupData(self):
        serial = Handle_Serial()
        self.send(serial, None)

    def _disconnect(self):
        Connection.connections.remove(self.connection)
        self.connection.close()
        self.state = Connection_State.disconnected
        print("Connection to host lost.")
    
    def send(self, message, payload):
        protocolSend(self.connection, message, payload)
    

def debugTerminal():
    while True:
        data = input("")


if __name__ == "__main__":
    connection = Connection(Config.SERVER_IP, Config.SERVER_PORT)
    connection.connect()

    debug_terminal_thread = threading.Thread(target=debugTerminal)
    debug_terminal_thread.start()