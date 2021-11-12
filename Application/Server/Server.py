import socket, ssl, threading, os
from DataFormatter import Protocol_Send, Protocol_ReceiveLength

def Deal_With_Client(connstream):
    while True:
        try:
            size = Protocol_ReceiveLength(connstream)                             #Recieve the bytes length of incoming data first
            data = connstream.recv(size)                                         #Receive raw encrypted data constantly           #Unencrypt the message
            print(f"From: Bytes:{size} Data:{data}")                             #For now just print the data stream
        except:
            print(f"{connstream} not connected")
            break
    
def Start_Server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="./Auth/certificate.pem", keyfile="./Auth/key.pem")
    
    bindsocket = socket.socket()
    bindsocket.bind(('localhost', 10023))
    bindsocket.listen(5)

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