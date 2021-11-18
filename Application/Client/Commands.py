from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
import os

def Send(message):       #Sends the message to the server
    Protocol_Send(Device.this_device.server, message)

def Set_Name(name):      #Sets our device name locally and on the server
    Device.this_device.name = name
    Protocol_Send(Device.this_device.server, f"set name {name}" )

def Set_Type(archetype): #Sets the device type locally and on the server
    Device.this_device.archetype = archetype
    Protocol_Send(Device.this_device.server, f"set type {archetype}")

def Self():              #Get info about this device
    print(Device.this_device)

def Run_Command(data, from_server):
    stream = os.popen(data)
    output = stream.read()
    if from_server:
        Protocol_Send(Device.this_device.server, output)
        print(f"{data} called from Server")
    else:
        print(output)
