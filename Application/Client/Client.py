import ssl, socket, threading
from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
from CommandHandler import Terminal_Command
import Config

#Connects to the server on given ip/port and creates send thread. We also send initial data to the server (Name/type)
def Connect(host, port):
    context = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
    context.load_verify_locations('./Auth/certificate.pem')                   #Load the cert so it will be accepted since it is self signed

    connection = context.wrap_socket(socket.socket(socket.AF_INET),           #Wrap the socket with TLS
                                    server_hostname=host)

    connection.connect((host, port))

    print(f"Connected to {host}:{port}")

    Protocol_Send(connection, device.name)                                                  #Send the device name TEMPORARILY setting to random number
    Protocol_Send(connection, device.archetype)                                             #Sending the device type
    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))              #Starting thread to recieve data
    receive_thread.start()

    return connection                                                                       #Returns the connection object


###Receives data from the given connection and runs it against client_command from serverhelper
def Receive_Data(connection):
    global connected
    while connected:
        try:
            message = Protocol_Receive(connection)    #Recieve message from server
            Terminal_Command(message,True)       #Checks for commands if no command is found prints to console.
        except:                                             
            print("Connection to host lost.")         #If no more data is flowing, we have disconnected from the server
            connected = False

###The terminal for hte client to enter commands and send data to server from
def Terminal(): 
    while True:                                                                                                                                                      
        try:
            data_input = input("\n")
            Terminal_Command(data_input, False)
        except Exception as e:
            print(e)


#PRE UI FUNCTIONALITY
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
