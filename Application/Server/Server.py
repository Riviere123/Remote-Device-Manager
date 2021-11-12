import socket, ssl, threading, os
from Device import Device
from DataFormatter import Protocol_Send, Protocol_Receive

### Each client will have there own Deal_With_Client Thread ##
### Client Commands ###
### set name (name) sets the devices name
### set type (type) sets the devices type
def Deal_With_Client(connstream):
    client_device = Device(connstream, Protocol_Receive(connstream), Protocol_Receive(connstream)) #Set the client_device to a newly created Device object.
    while True:                                                                                    #Set device name and archetype with first 2 recieved data
        try:
            data = Protocol_Receive(connstream)                                      #data = Recieved data
            if data[:8].lower() == "set name":                                       #If the first 8 characters from the recieved data is "set name"       
                split_data = data.split(" ")                                         #Split the data by spaces         
                new_name = split_data[2]                                             #Take the third position as the new name                              
                print(f"{client_device.name}'s name has been changed to {new_name}") 
                client_device.Change_Name(new_name)                                  #calls the change name method from the device
            elif data[:8].lower() == "set type":                                     #If the first 8 characters from the recieved data is "set type"
                split_data = data.split(" ")  
                new_type = split_data[2]                                             #Take the third position as the new name 
                print(f"{client_device.name}'s device type changed to {new_type}")   
                client_device.archetype = new_type                                   #Set archetype of the Device object of the client  
                
            
            else:
                print(f"{client_device.name}: {data}")                               #For now just print the data stream

        except:
            print(f"{connstream} Disconnected")                                      #Client disconnected   
            break

### Starts the Terminal and allows commands to be entered from the server ###
### Commands ###
### list - Lists all stored devices names and types
### Send (Device) (Message) - Sends the message to the device client
def Terminal():                                                                                                                                                      
    while True:                                                                                                                                                      
        command = input("").split(" ")                                                                                                                               
        if command[0].lower() == "send":     
            try:
                Protocol_Send(Device.devices[command[1]].client, " ".join(command[2:]))
            except:
                print("Error: Client doesn't exist by that name.")
        if command[0].lower() == "list":
            [print(f"Name:{Device.devices[i].name} Type:{Device.devices[i].archetype}") for i in Device.devices.keys()]

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

            thread = threading.Thread(target=Deal_With_Client, args=(connstream,))          #Creating a thread for each client                                                            
            thread.start()                                                                  #Starting the thread, each connection will start a new thread 
        except:
            print("Connection failed.")


if __name__ == "__main__":
    server_thread = threading.Thread(target=Start_Server, args=('localhost', 10023))        #Start the server
    server_thread.start()