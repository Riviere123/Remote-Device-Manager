###Formats the recieved data to first collect the message size then return the message with the right size
def Protocol_Receive(connection):     
    data = ""              
    length = int(connection.recv(10))                #Every message comes prefaced with a 10 bit size.
    while length >= 1024:
        message = connection.recv(1024)
        data += message.decode()
        length -= 1024
    if length > 0:                                   #If the length of the message is still greater than 0
        message = connection.recv(length)            #Receive the remainder of the message
        data += message.decode()
        length = 0
    return data                                      #Return the message

###Sends the length of the message then the message itself
def Protocol_Send(connection, message):
    try:
        if message == "":
            return
        if type(message) == str:                      
            message = message.encode()                #Encode the string 
            length = str(len(message)).zfill(10)      #Get the length of the string and make the number 10 digits regardless
        connection.send(length.encode())              #Send the length of the next data block
        connection.send(message)                      #Send the datablock
    except Exception as e:
        print(e)