from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
import os

#Sends the message to the server
def Send(message):       
    Protocol_Send(Device.this_device.server, message)

#Sets our device name locally and on the server
def Set_Name(name):      
    Device.this_device.name = name
    Protocol_Send(Device.this_device.server, f"set name {name}" )

#Sets the device type locally and on the server
def Set_Type(archetype): 
    Device.this_device.archetype = archetype
    Protocol_Send(Device.this_device.server, f"set type {archetype}")

#Get info about this device
def Self():              
    print(Device.this_device)

#Run a terminal command on this device
def Run_Command(data, from_server):
    stream = os.popen(data)
    output = stream.read()
    if from_server:                                        #If the command was from the server send the output to the server
        Protocol_Send(Device.this_device.server, output)
        print(f"{data} called from Server")
    else:                                                  #otherwise just print to the console
        print(output)
