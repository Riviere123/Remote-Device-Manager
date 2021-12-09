###Formats the recieved data to first collect the message size then return the message with the right size
def Protocol_Receive(connection):    
    data = ""              
    length = int(connection.recv(10))                #Every message comes prefaced with a 10 bit size.
    while length >= 1024:
        message = connection.recv(1024)
        data += message.decode()
        length -= 1024
    if length > 0:
        message = connection.recv(length)
        data += message.decode()
        length = 0


    return data

###Sends the length of the message then the message itself
def Protocol_Send(connection, message):
    try:
        if message == "":
            return
        if type(message) == str:                      #make sure our message is a string
            message = message.encode()         #Encode the string 
            length = str(len(message)).zfill(10)       #Get the length of the string and make the number 4 digits regardless
        connection.sendall(length.encode())           #Send the length of the next data block
        connection.sendall(message)                          #Send the datablock
    except Exception as e:
        print(e)
