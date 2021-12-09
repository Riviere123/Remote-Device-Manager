import socket, ssl, threading
from Device import Device
from DataFormatter import Protocol_Send, Protocol_Receive
from Command.CLI_Command_Handler import Client_Command, Server_Terminal
import Config
from Flask_Wrapper import flask_server    

### Each client will have their own Deal_With_Client Thread ###
def Deal_With_Client(connstream):
    device_setup_message = Protocol_Receive(connstream).split(" ")        #Recieve the first message from the client
    device_name = device_setup_message[0]                                 #Pull the device name
    device_archetype = device_setup_message[1]                            #Archetype
    device_id = device_setup_message[2]                                   #Id
    device_serial = device_setup_message[3]                               #Serial
    device_platform = device_setup_message[4]                             #OS information
    entered_password = device_setup_message[5]                            #Password passed to the server
    if entered_password == Config.SERVER_PASSWORD:
        #TODO Optomise
        found = False
        for device in Device.devices:
            client_device = Device.devices[device]
            if client_device.serial == device_serial:                             #If that device has connected before based on there serial number                                           #Set the device to the existing device
                client_device.name = device_name                                  #Set the device name to clients devices name
                client_device.archetype = device_archetype                        #Archetyp
                client_device.client = connstream                                 #Set the new connection as the devices client
                Protocol_Send(connstream, f"set id {client_device.id}")           #Send the same Id back to the client
                found = True
        if not found:                                                                 #Otherwise if it is a never before connected device
            client_device = Device(connstream, device_name, device_archetype, device_id, device_serial, device_platform) #Set the client_device to a newly created Device object.
            Protocol_Send(connstream, f"set id {client_device.id}")                                  #Send the generated id to the device(The device will then store this id)

        while True:
            try:
                data = Protocol_Receive(connstream)       #data = any messages from the client
                Client_Command(client_device, data)       #Checks if there is any commands in the message and reacts accordingly
            except:                                       #Client is disconnected
                client_device.client.close()              #Close the clients connection                 
                client_device.client = None               #Set the devices client to None(This is appropriate for seeing if the client is connected or not)
                print(f"{client_device}")    #Print that the client has disconnected
                break                                     #End the thread
    else:
        Protocol_Send(connstream, f"failed to connect")
        connstream.close()

### Starts the Terminal and allows commands to be entered from the server ###
def Terminal():                                                                                                                                                     
    while True:                         
        Server_Terminal()                                                                                                                             

#starts the server with the provided IP and Port
def Start_Server(host, port):
    bindsocket = socket.socket()                                                          
    bindsocket.bind((host, port))                                                         #binding the socket and port
    bindsocket.listen()                                                                   #listening on that port

    terminal_thread = threading.Thread(target=Terminal)                                   #Create the terminal thread
    terminal_thread.start()                                                               #Start terminal thread
    print("Listening for connections... \n")

    while True:          ########We could introduce a peering button that only accepts connections when active.(Would need to figure out how to handle reconnecting of devices got this use case)
        try:
            client, addr = bindsocket.accept()                                              #Accept clients and assign pull client and ip
            connstream = context.wrap_socket(client, server_side=True)                      #Wrap the socket with TLS
            print(f"Device connected from {addr}")
            thread = threading.Thread(target=Deal_With_Client, args=(connstream,))          #Creating a thread for each client                                                            
            thread.start()                                                                  #Starting the thread, each connection will start a new thread 
        except Exception as e:
            print(f"{e} Connection failed.")

if __name__ == "__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)                                                   #Setting context to default client_auth context
    context.load_cert_chain(certfile="./Auth/certificate.pem", keyfile="./Auth/key.pem", password=Config.PASSWORD)  #Loads the Certificate and Key

    server_thread = threading.Thread(target=Start_Server, args=(Config.IP_ADDRESS, Config.PORT))                    #Start the server
    server_thread.start()

    flask_server.run(ssl_context=context, debug=False, port=Config.FLASK_PORT)                                      #Start the flask server