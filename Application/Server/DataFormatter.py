def Protocol_ReceiveLength(connection):                  #Every message comes prefaced with a 4 bit size.
    return int(connection.recv(4))

def Protocol_Send(connection, message):
    if type(message) == str:                      #make sure our message is a string
        message = message.encode('ascii')         #Encode the string 
        length = str(len(message)).zfill(4)       #Get the length of the string and make the number 4 digits regardless

    else:
        length = str(len(message)).zfill(4)

    connection.send(length.encode('ascii'))           #Send the length of the next data block
    connection.send(message)                          #Send the datablock
