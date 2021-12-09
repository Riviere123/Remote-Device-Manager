from Device import Device
from DataFormatter import Protocol_Receive, Protocol_Send
from subprocess import PIPE, Popen


def Send(message):       
    Protocol_Send(Device.this_device.server, message)

#Sets our device name locally and on the server
def Set_Name(name, from_server):
    if from_server:  
        Device.this_device.name = name
        return({"message": f"Name changed to {name}. Called from server."})
    if not from_server:
        Device.this_device.name = name
        Device.this_device.id
        Protocol_Send(Device.this_device.server, f"set name {name}")
        return({"message": f"Name changed to {name}."})

#Sets the device type locally and on the server
def Set_Type(archetype, from_server):
    if from_server:
        Device.this_device.archetype = archetype
        return({"message": f"Type changed to {archetype}. Called from server."})
    if not from_server:
        Device.this_device.archetype = archetype
        Protocol_Send(Device.this_device.server, f"set type {archetype}")
        return({"message": f"Type changed to {archetype}."})

def Set_Id(id, from_server):
    if from_server:
        Device.this_device.id = id
        return({"message": f"client id set to {id}."})

#Get info about this device
def Self():              
    return({"message": Device.this_device})

#Run a terminal command on this device
def Run_Command(data, from_server):
    try:
        p = Popen(data, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        payload = f"#|#stdout {stdout.decode()} #|#stderr {stderr.decode()}"
        if from_server:
            Protocol_Send(Device.this_device.server,f"run output " + payload)
            return({"message": f"{data} called from Server"})
        else:
            return({"message": payload})
    except Exception as e:
        print(e)

#sends the devices modules data to the server
def Send_Mod_Data():
    Device.this_device.Send_Module_data()
    return({"message": "Mod data sent"})

def Start_Camera():
    for mod in Device.this_device.modules:
        if mod.archetype == "camera":
            mod.Start_Camera()
            return({"message": f"Camera on {mod.name} ended"})
    return({"message": "No camera found"})

def Stop_Camera():
    for mod in Device.this_device.modules:
        if mod.archetype == "camera":
            mod.Stop_Camera()