from random import randrange
import ssl, socket, threading
from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
from ServerHelper import Client_Command
from CommandHandler import Terminal_Command
import Config

def Connect(host, port):
    context = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
    context.load_verify_locations('./Auth/certificate.pem')                   #Load the cert so it will be accepted since it is self signed

    connection = context.wrap_socket(socket.socket(socket.AF_INET),           #Wrap the socket with TLS
                                    server_hostname=host)

    connection.connect((host, port))

    print(f"Connected to {host}:{port}")

    Protocol_Send(connection, device.name)                                      #Send the device name TEMPORARILY setting to random number
    Protocol_Send(connection, device.archetype)                                            #Sending the device type
    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))   #Starting thread to recieve data
    receive_thread.start()

    return connection                                                                       #Returns the connection object


###Receives data from the given connection
def Receive_Data(connection):
    global connected
    while connected:
        try:
            message = Protocol_Receive(connection)
            Client_Command(connection, message)
        except:                                             
            print("Connection to host lost.")
            connected = False


###Sends data to the given connection
def Send_Data(connection, message):                               
    Protocol_Send(connection, message)

def Terminal():
    while True:                                                                                                                                                      
        try:
            Terminal_Command()
        except Exception as e:
            print(e)

    
if __name__ == "__main__":
    name = input("Name your device: ").lower()
    archetype = input("Give your device a type: ").lower()
    device = Device(name, archetype)
    connected = False
    terminal_thread = threading.Thread(target=Terminal)
    terminal_thread.start()
    while True:
        if connected == False:
            try:
                connected = True
                connection = Connect(Config.SERVER_IP, Config.SERVER_PORT)
                device.server = connection
            except:
                connected = False
                print("Failed to connect. Trying again...")
