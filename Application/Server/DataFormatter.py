###Formats the recieved data to first collect the message size then return the message with the right size
def Protocol_Receive(connection):                   
    length = int(connection.recv(4))                #Every message comes prefaced with a 4 bit size.
    return connection.recv(length).decode()         #Return the 

###Sends the length of the message then the message itself
def Protocol_Send(connection, message):
    try:
        if message == "":
            return
        if type(message) == str:                          #make sure our message is a string
            message = message.encode('ascii')             #Encode the string 
            length = str(len(message)).zfill(4)           #Get the length of the string and make the number 4 digits regardless

        connection.send(length.encode('ascii'))           #Send the length of the next data block
        connection.send(message)                          #Send the datablock
    except Exception as e:
        print(e)
