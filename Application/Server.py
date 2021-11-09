import threading
import socket
import Config
from Device import Device

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #Create the server socket
server.bind((Config.Host, Config.Port))                        #Bind the ip and port from Config.py
server.listen()                                                #Start listening to connections

def Broadcast(message):                            #Send a message to every device registered
    for device in Device.devices:
        device.client.send(message)

def SendMessage(device, message):                  #Send a message to specific device
    device.client.send(message)                    

def Handle(client):
    while True:
        try:
            data = client.recv(1024)               #Receive data constantly
            print(data.decode())                   #For now just print the data stream
        except:
            print(f"{client} not connected")
            break

def Recieve():
    while True:
        client, address = server.accept()                                   #Accept incoming connection setting client and address from connection

        name = client.recv(1024).decode('ascii')                            #Receive device name from client
        archetype = client.recv(1024).decode('ascii')                       #Receive device Archetype from client
        device = Device(client, name, archetype)                            #Create the Device object
        print(f"{device.name} connected from {address}")                    
        device.client.send("Connected to the server.".encode('ascii'))      #Send message to the new client
        
        thread = threading.Thread(target=Handle, args=(client,))            #Creating a thread of the Handle function and passing the client argument in                                                             
        thread.start()                                                      #Starting the thread, each connection will start a new thread 

print("Server is listening...")
Recieve() #Start the server (Potential to make this asynchonous along with Broadcast and SendMessage to test sending commands to clients)