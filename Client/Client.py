import ssl, socket, threading, Config
from Protocols import protocolReceive
from enum import Enum


class Connection_State(Enum):
    connecting = 0
    connected = 1
    disconnected = 2

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
                #What to do with the data?!
                print(data)
            except:                             
                self.disconnect()             
                break

    def connect(self):
        self.state = Connection_State.connecting
        certificate = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
        certificate.load_verify_locations('./Authentication/certificate.pem')                   #Load the cert so it will be accepted since it is self signed
        connection = certificate.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host)
        connection.connect((self.host, self.port))
        self.connection = connection
        Connection.connections.append(connection)
        self.state = Connection_State.connected
        print(f"Connected to {self.host}:{self.port}")
        receive_thread = threading.Thread(target=self.handleConnection, args=(connection,))              #Create and start a thread to recieve data
        receive_thread.start()

    
    def disconnect(self):
        Connection.connections.remove(self.connection)
        self.connection.close()
        self.state = Connection_State.disconnected
        print("Connection to host lost.")
        
if __name__ == "__main__":
    connection = Connection(Config.SERVER_IP, Config.SERVER_PORT)
    connection.connect()