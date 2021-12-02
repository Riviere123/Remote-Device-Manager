import string, random
import Config
def Generate_Serial(length):
    letters = [char for char in (string.ascii_uppercase + string.ascii_lowercase + "1234567890")]
    serial = []
    for x in range(0,length):
        serial.append(random.choice(letters))

    return("".join(serial))

def Handle_Serial(length):
    try:
        with open("./Auth/serial.txt", "r") as f:
            Config.SERIAL = f.read()
    except:
        Generate_Serial
        with open("./Auth/serial.txt", "w") as f:
            Config.SERIAL = Generate_Serial(length)
            f.write(Config.SERIAL)


if __name__ == "__main__":
    Handle_Serial(Config.SERIAL_LENGTH)
    print(Config.SERIAL)
