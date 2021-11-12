import ssl, socket, threading
from DataFormatter import Protocol_ReceiveLength, Protocol_Send



def Connect(host, port):
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                        server_hostname=host)

    conn.connect((host, port))
    cert = conn.getpeercert()

    return conn

def Receive_Data(connection):                                    #Handles the receiving of messages from the server
    while True:
        try:
            size = Protocol_ReceiveLength(connection)        #Get the size of the message
            message = connection.recv(size).decode()        #Recieve messages from server
            print(message)                                  #Print the message.

        except:                                       #We will add the ability to issue commands to the device from the server
            print("An error occurred! you may have lost connection.")
            connection.close()                        #If we lose connection close the connection.
            break

def Send_Data(connection):                                      #Send Data to the server
    while True:
        message = input("Write a message: ").encode('ascii')
        Protocol_Send(connection, message)                     #Send the message using my protocol



if __name__ == "__main__":
    context = ssl.create_default_context()
    context.load_verify_locations('./Auth/certificate.pem')

    connection = Connect("localhost", 10023)

    receive_thread = threading.Thread(target=Receive_Data, args=(connection,))  #Creates and starts a thread for receiving data
    receive_thread.start()

    send_thread = threading.Thread(target=Send_Data, args=(connection,))      #Creates and starts a thread for sending data
    send_thread.start()