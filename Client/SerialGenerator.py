import string, random, Config

def Generate_Serial(length): #Given a length generates a serial number of that length
    letters = [char for char in (string.ascii_uppercase + string.ascii_lowercase + "1234567890")]
    serial = []
    for x in range(0,length):
        serial.append(random.choice(letters))

    return("".join(serial))

def Handle_Serial():
    try:                                           #If serial.txt already exists, pull the serial number from the file
        with open("./Authentication/serial.txt", "r") as f: 
            return f.read()
            
    except:
        Generate_Serial                            #If the file doesn't exist write to a new serial.txt file a new generated serial
        with open("./Authentication/serial.txt", "w") as f:
            serial = Generate_Serial(Config.SERIAL_LENGTH)
            f.write(serial)
            return serial


#NOTE: Below is for testing and is not needed.
if __name__ == "__main__":
    Handle_Serial()
    print(Config.SERIAL)