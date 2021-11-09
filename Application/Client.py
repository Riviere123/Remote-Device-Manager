import socket
import threading

import time   #Import time for delaying test messages

name = input("Name: ")                   #Need to figure out a way to assign device names
archetype = input("Archetype: ")         #Need to figure out how we will pass what sensors/attachment are on the device.


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create the client socket
client.connect(('localhost', 8811))                          #Connect the client to the server

client.send(f"{name}".encode('ascii'))                       #Send the name of the device to the server
client.send(f"{archetype}".encode('ascii'))                  #Send the archetype to the server

def Receive():                                    #Handles the receiving of messages from the server
    while True:
        try:
            message = client.recv(1024).decode()  #Recieve messages from server
            print(message)                        #Simply print the message. 
        except:                                   #We will add the ability to issue commands to the device from the server
            print("An error occurred! you may have lost connection.")
            client.close()                        #If we lose connection close the connection.
            break

def Write():                                    #Send Data to the server
    while True:                                 
        message = f"{name}: Data"               #Sample data
        time.sleep(5)                           #Sleep 5 seconds so we don't flood the server while testing
        client.send(message.encode('ascii'))    #Send the data to the server

                                                   ##Threads allow us to Asynchronously run the Receive and write method 
receive_thread = threading.Thread(target=Receive)  #Creates and starts a thread for receiving data
receive_thread.start()

write_thread = threading.Thread(target=Write)      #Creates and starts a thread for sending data
write_thread.start()