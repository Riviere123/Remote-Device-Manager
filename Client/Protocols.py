import pickle
from datetime import datetime
class Message():
    def __init__(self, message, payload):
        self.message = message
        self.payload = payload
        self.time = datetime.now()

def protocolSend(connection, message, payload):
    message = Message(message, payload)
    packaged_data = pickle.dumps(message)
    length = str(len(packaged_data)).zfill(10)
    connection.send(length.encode())
    connection.send(packaged_data)

def protocolReceive(connection):
    length = int(connection.recv(10))
    packaged_data = connection.recv(length)
    message = pickle.loads(packaged_data)
    return message