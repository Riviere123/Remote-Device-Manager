import ssl, socket, threading, getpass
from Device import Device, Module
from DataFormatter import Protocol_Receive, Protocol_Send
from Command.Command_Handler import Client_Terminal, Server_Data_Processor
from SerialGeneration import Handle_Serial
import Config

#Connects to the server on given ip/port and creates send thread. We also send initial data to the server (Name/type)
def Connect(host, port, password):
    context = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
    context.load_verify_locations('./Auth/certificate.pem')                   #Load the cert so it will be accepted since it is self signed

    connection = context.wrap_socket(socket.socket(socket.AF_INET),           #Wrap the socket with TLS
                                    server_hostname=host)

    connection.connect((host, port))                                          #Connect to the server

    print(f"Connected to {host}:{port}")

    device_setup_message = f"{device.name} {device.archetype} {device.id} {device.serial} {device.os_platform} {password}"                  #Create the setup message
    Protocol_Send(connection, device_setup_message)                                         #Send the device setup message

    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))              #Create and start a thread to recieve data
    receive_thread.start()

    return connection                                                                       #Returns the connection object


###Receives data from the given connection and runs it against client_command from serverhelper
def Receive_Data(connection):
    global connected
    while connected:                                  #If we have an active connection
        try:
            data = Protocol_Receive(connection)    #Recieve data from server
            Server_Data_Processor(data)            #Checks for commands if no command is found prints to console.
        except:                                             
            print("Connection to host lost.")         #If no more data is flowing, we have disconnected from the server
            connected = False                         #Set connected to false

###The terminal for the client to enter commands and send data to server from
def Terminal(): 
    while True:                                                                                                                                                      
        Client_Terminal()


#PRE UI FUNCTIONALITY
if __name__ == "__main__":
    name = input("Name your device: ").lower()                  #set name
    archetype = input("Give your device a type: ").lower()      #set archetype
    password = getpass.getpass('Password:')
    Handle_Serial(Config.SERIAL_LENGTH)
    device = Device(name, archetype, Config.SERIAL)                            #create device object
    ####MODULE TESTING
    camera_module = Module(device, "Home_Camera", "camera")
    device.Attach_Module(camera_module)
    #########
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


