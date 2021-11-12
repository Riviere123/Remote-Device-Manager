import socket, ssl, threading, os
from Device import Device
from DataFormatter import Protocol_Send, Protocol_Receive

def Deal_With_Client(connstream):
    client_device = Device(connstream, Protocol_Receive(connstream), Protocol_Receive(connstream))
    while True:
        try:
            data = Protocol_Receive(connstream)                             #Recieve the bytes length of incoming data first
            if data[:8].lower() == "set name":
                split_data = data.split(" ")
                new_name = split_data[2]
                print(f"{client_device.name}'s name has been changed to {new_name}")
                client_device.Change_Name(new_name)
            elif data[:8].lower() == "set type":
                new_type = data[9:]
                print(f"{client_device.name}'s device type changed to {new_type}")
                client_device.archetype = data[9:]
                
            
            else:
                print(f"\nFrom: {client_device.name} Data: {data}")                                           #For now just print the data stream


        except:
            print(f"{connstream} not connected")
            break

def Terminal():
    while True:
        command = input("").split(" ")
        if command[0].lower() == "send":
            try:
                Protocol_Send(Device.devices[command[1]].client, " ".join(command[2:]))
            except:
                print("Error: Client doesn't exist by that name.")


def Start_Server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="./Auth/certificate.pem", keyfile="./Auth/key.pem")
    
    bindsocket = socket.socket()
    bindsocket.bind(('localhost', 10023))
    bindsocket.listen()
    
    terminal_thread = threading.Thread(target=Terminal) #Start the terminal
    terminal_thread.start()
    print("Listening for connections... \n")

    while True:
        try:
            client, addr = bindsocket.accept()
            connstream = context.wrap_socket(client, server_side=True)

            thread = threading.Thread(target=Deal_With_Client, args=(connstream,))          #Creating a thread for each client                                                            
            thread.start()                                                                  #Starting the thread, each connection will start a new thread 
        except:
            print("Connection failed.")


if __name__ == "__main__":
    server_thread = threading.Thread(target=Start_Server) #Start the server
    server_thread.start()