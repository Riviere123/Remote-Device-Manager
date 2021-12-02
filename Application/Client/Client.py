import ssl, socket, threading
from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
from Commands import CLI_Command_Handler
from serialgeneration import Handle_Serial
import Config

#Connects to the server on given ip/port and creates send thread. We also send initial data to the server (Name/type)
def Connect(host, port, password):
    context = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
    context.load_verify_locations('./Auth/certificate.pem')                   #Load the cert so it will be accepted since it is self signed

    connection = context.wrap_socket(socket.socket(socket.AF_INET),           #Wrap the socket with TLS
                                    server_hostname=host)

    connection.connect((host, port))                                          #Connect to the server

    print(f"Connected to {host}:{port}")

    device_setup_message = f"{device.name} {device.archetype} {device.id} {device.serial} {password}"                  #Create the setup message
    Protocol_Send(connection, device_setup_message)                                         #Send the device setup message

    # Device.this_device.id=Protocol_Receive(connection)                                      #Receieve and set the id. If the device id was anything but -1 you will recieve the same id as you had sent.

    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))              #Create and start a thread to recieve data
    receive_thread.start()

    return connection                                                                       #Returns the connection object


###Receives data from the given connection and runs it against client_command from serverhelper
def Receive_Data(connection):
    global connected
    while connected:                                  #If we have an active connection
        try:
            message = Protocol_Receive(connection)    #Recieve message from server
            CLI_Command_Handler.Terminal_Command(message,True)            #Checks for commands if no command is found prints to console.
        except:                                             
            print("Connection to host lost.")         #If no more data is flowing, we have disconnected from the server
            connected = False                         #Set connected to false

###The terminal for the client to enter commands and send data to server from
def Terminal(): 
    while True:                                                                                                                                                      
        try:
            data_input = input("\n")
            CLI_Command_Handler.Terminal_Command(data_input, False)
        except Exception as e:
            print(e)


#PRE UI FUNCTIONALITY
if __name__ == "__main__":
    name = input("Name your device: ").lower()                  #set our name
    archetype = input("Give your device a type: ").lower()      #set our archetype
    password = input("Give the server password. ")              #The servers password
    Handle_Serial(Config.SERIAL_LENGTH)
    device = Device(name, archetype, Config.SERIAL)                            #create our device object
    connected = False                                           #Initialize connected bool
    terminal_thread = threading.Thread(target=Terminal)         #Create and start the terminal thread
    terminal_thread.start()
    while True:
        if connected == False:                                                 #If we are not connected.
            try:                                                               #Constantly try to reconnect to the server
                connected = True
                connection = Connect(Config.SERVER_IP, Config.SERVER_PORT, password)
                device.server = connection
            except:                                                            #If we fail to connect set connected to false so we try again
                connected = False
                print("Failed to connect. Trying again...")


