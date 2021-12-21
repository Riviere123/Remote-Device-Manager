import socket, ssl, threading, Config
from Protocols import protocolReceive
from Clients import Client
from Commands import CLIParser


#TODO: Have base class server
#inherit from that class
class Server():
    servers = []
    def __init__(self, name, certificate, ip, port):
        self.name = name
        self.certificate = certificate
        self.ip = ip
        self.port = port
        Server.servers.append(self)

    def startServer():
        pass

    def _handleConnection(self, connection, address):
        pass

class Connection_Server(Server):
#TODO DOCSTRINGS - class PEP257 Look for pep8 packages    pip package flake8
    def __init__(self, name, certificate, ip, port):
        super().__init__(name, certificate, ip, port)
#TODO DOCSTRING __init__
    def startServer(self):
        bindsocket = socket.socket()                                                          
        bindsocket.bind((self.ip, self.port))                                                      
        bindsocket.listen()                                                                                                             
        print("Listening for connections... \n")
        while True:     
            client, address = bindsocket.accept()
            connection = self.certificate.wrap_socket(client, server_side=True) 
            print(f"Device connected from {address}")
            thread = threading.Thread(target=self._handleConnection, args=(connection, address))                                                           
            thread.start()   

    def _handleConnection(self, connection, address):
        client = self._clientSetup(connection, address)
        try:
            while True:
                message = protocolReceive(connection)
                #TODO: Implement Client message parsing
                print(message.time, message.message, message.payload)
        except:
            client.disconnect()
            print("client disconnected.")        

    def _clientSetup(self, connection, address):
        initial_client_message =  protocolReceive(connection)
        serial_number = initial_client_message.message
        client = Client.clientSetup(connection, address, serial_number)
        return client    
                                            
class Terminal():
    def start(self):
        while True:
            cli_input = input("") 
            command_result = CLIParser.parse(cli_input)
            if command_result.payload != None:
                print(command_result.payload)                                                                                                      
    

if __name__ == "__main__":
    certificate = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)                                                   
    certificate.load_cert_chain(certfile="./Authentication/certificate.pem", keyfile="./Authentication/key.pem", password=Config.PASSWORD)

    connection_server = Connection_Server("Connection Server", certificate,Config.IP_ADDRESS, Config.PORT)
    connection_server_thread = threading.Thread(target=connection_server.startServer)                    
    connection_server_thread.start()

    terminal = Terminal()

    terminal_thread = threading.Thread(target=terminal.start)
    terminal_thread.start()
