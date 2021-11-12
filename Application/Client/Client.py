from random import randrange
import ssl, socket, threading
from DataFormatter import Protocol_Receive, Protocol_Send
import random



def Connect(host, port):
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                        server_hostname=host)

    conn.connect((host, port))
    cert = conn.getpeercert()

    print(f"Connected to {host}:{port}")

    Protocol_Send(conn, str(random.randrange(0,10000)))
    Protocol_Send(conn, "DeviceArchetype")

    return conn

def Receive_Data(connection):
    while True:
        try:
            message = Protocol_Receive(connection)       
            print("\n" + message)                                 

        except:                                             
            print("Connection to host lost.")
            connection.close()   
            break

def Send_Data(connection):                                      
    while True:
        message = input("Write a message: ")
        Protocol_Send(connection, message)                    

if __name__ == "__main__":
    context = ssl.create_default_context()
    context.load_verify_locations('./Auth/certificate.pem')

    connection = Connect("localhost", 10023)

    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))  
    receive_thread.start()

    send_thread = threading.Thread(target=Send_Data, args=(connection,))    
    send_thread.start()