import socket, ssl, threading, os
from Device import Device
from DataFormatter import Protocol_Send, Protocol_Receive
from Commands import Client_Command, Server_Command

### Each client will have there own Deal_With_Client Thread ##
def Deal_With_Client(connstream):
    client_device = Device(connstream, Protocol_Receive(connstream), Protocol_Receive(connstream)) #Set the client_device to a newly created Device object.
    while True:                                                                                    #Set device name and archetype with first 2 recieved data
        try:
            data = Protocol_Receive(connstream)                                      #data = Recieved data
            Client_Command(client_device, data)                                      #Checks the command and reacts accordingly.
        except:
            print(f"{connstream} Disconnected")                                      #Client disconnected   
            break

### Starts the Terminal and allows commands to be entered from the server ###
def Terminal():                                                                                                                                                      
    while True:                         
        Server_Command()                                                                                                                             

#starts the server with the provided IP and Port
def Start_Server(host, port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)                         #Setting context to default client_auth context
    context.load_cert_chain(certfile="./Auth/certificate.pem", keyfile="./Auth/key.pem")  #Loads the Certificate and Key
    
    bindsocket = socket.socket()                                                          
    bindsocket.bind((host, port))                                                        #binding the socket and port
    bindsocket.listen()                                                                  #listening on that port
    
    terminal_thread = threading.Thread(target=Terminal)                                  #Create the terminal thread
    terminal_thread.start()                                                              #Start terminal thread
    print("Listening for connections... \n")

    while True:
        try:
            client, addr = bindsocket.accept()                                              #Accept clients and assign pull client and ip
            connstream = context.wrap_socket(client, server_side=True)                      #Wrap the socket with TLS
            print(f"Device connected from {addr}")
            thread = threading.Thread(target=Deal_With_Client, args=(connstream,))          #Creating a thread for each client                                                            
            thread.start()                                                                  #Starting the thread, each connection will start a new thread 
        except:
            print("Connection failed.")


if __name__ == "__main__":
    server_thread = threading.Thread(target=Start_Server, args=('localhost', 10023))        #Start the server
    server_thread.start()