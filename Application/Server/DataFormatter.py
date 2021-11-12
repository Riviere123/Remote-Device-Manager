def Protocol_Receive(connection):                  #Every message comes prefaced with a 4 bit size.
    length = int(connection.recv(4))
    return connection.recv(length).decode()

def Protocol_Send(connection, message):
    try:
        if message == "":
            return
        if type(message) == str:                      #make sure our message is a string
            message = message.encode('ascii')         #Encode the string 
            length = str(len(message)).zfill(4)       #Get the length of the string and make the number 4 digits regardless

        else:                                         #If the message is already encoded(which it should not be)
            length = str(len(message)).zfill(4)

        connection.send(length.encode('ascii'))           #Send the length of the next data block
        connection.send(message)                          #Send the datablock
    except:
        print("There was an error sending data from Protocol_Send within DataFormatter. You may have used unsupported special characters")
