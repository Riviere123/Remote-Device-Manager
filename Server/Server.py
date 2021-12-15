import socket, ssl, threading, Config
from Protocols import protocolReceive
from Clients import Client
from Commands import Parser
from Commands import Command, Formats

class Server():
    servers = []
    def __init__(self, name, certificate, ip, port):
        self.name = name
        self.certificate = certificate
        self.ip = ip
        self.port = port
        Server.servers.append(self)

    def startServer(self):
        bindsocket = socket.socket()                                                          
        bindsocket.bind((self.ip, self.port))                                                      
        bindsocket.listen()                                                                                                             
        print("Listening for connections... \n")
        while True:     
            client, addr = bindsocket.accept()
            connection = self.certificate.wrap_socket(client, server_side=True) 
            print(f"Device connected from {addr}")
            thread = threading.Thread(target=self.handleConnection, args=(connection,))                                                           
            thread.start()   

    def handleConnection(self, connection):
        client = Client(connection)
        try:
            while True:
                data = protocolReceive(connection)
                #IOT MESSAGE PARSING
                print(data.message)
        except:
            client.disconnect()
            print("client disconnected.")                                                         

def terminal():                                                                                                                                                
    while True:
        cli_input = input("")
        cli_parser = Parser(cli_input, Formats.CLI)
        cli_parser.parse()
        print(cli_parser.runAndStyle())

if __name__ == "__main__":
    certificate = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)                                                   
    certificate.load_cert_chain(certfile="./Authentication/certificate.pem", keyfile="./Authentication/key.pem", password=Config.PASSWORD)

    connection_server = Server("Connection Server", certificate,Config.IP_ADDRESS, Config.PORT)
    onnection_server_thread = threading.Thread(target=connection_server.startServer)                    
    onnection_server_thread.start()
    terminal_thread = threading.Thread(target=terminal)
    terminal_thread.start()
