import string, random

def Generate_Serial(length):
    letters = [char for char in (string.ascii_uppercase + string.ascii_lowercase + "1234567890")]
    serial = []
    for x in range(0,length):
        serial.append(random.choice(letters))

    print("".join(serial))
