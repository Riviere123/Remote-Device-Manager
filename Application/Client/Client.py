from random import randrange
import ssl, socket, threading
from DataFormatter import Protocol_Receive, Protocol_Send
from CommandHelper import Client_Command


###Connects to the host on the given port
def Connect(host, port):
    conn = context.wrap_socket(socket.socket(socket.AF_INET),    #Wrap the socket with TLS
                                        server_hostname=host)

    conn.connect((host, port))
    # cert = conn.getpeercert()                                     #save the cert as cert variable

    print(f"Connected to {host}:{port}")

    Protocol_Send(conn, str(randrange(0,10000)))            #Send the device name TEMPORARILY setting to random number
    Protocol_Send(conn, "DeviceArchetype")                         #Sending the device type

    return conn                                                    #Returns the connection object

###Receives data from the given connection
def Receive_Data(connection):
    while True:
        try:
            message = Protocol_Receive(connection)
            Client_Command(connection, message)
        except:                                             
            print("Connection to host lost.")
            connection.close()
            break

###Sends data to the given connection
def Send_Data(connection):                                      
    while True:
        message = input("")
        Protocol_Send(connection, message)                    


if __name__ == "__main__":
    context = ssl.create_default_context()                                    #helps create SSLContext objects for common purposes
    context.load_verify_locations('./Auth/certificate.pem')                   #Load the cert so it will be accepted since it is self signed

    connection = Connect("localhost", 10023)

    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))   #Starting thread to recieve data
    receive_thread.start()

    send_thread = threading.Thread(target=Send_Data, args=(connection,))         #Starting thread to send data
    send_thread.start()