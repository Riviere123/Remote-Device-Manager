import pickle
class Message():
    def __init__(self, message):
        self.message = message

def protocolSend(connection, data):
    message = Message(data)
    data = pickle.dumps(message)
    length = str(len(data)).zfill(10)
    connection.send(length.encode())
    connection.send(data)

def protocolReceive(connection):
    length = int(connection.recv(10))
    data = connection.recv(length)
    data = pickle.loads(data)
    return data