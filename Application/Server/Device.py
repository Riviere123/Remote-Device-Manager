import cv2

#NOTE:Device Information
# devices - a dictionary of every device (key:device_id|value:device object)
# count - used to asign a new id. increments everytime a new unrecognized device connects
#----------------------------------
# client - the client stream object used to send and recieve data
# name - the name of the device
# archetype - the type/description of the device
# id - the devices id used to find the device in devices dictionary if the device passes a -1 as the id we assign it a new id
# serial - the serial number of the device this is passed from the client upon connecting
# run_command_output - the last output of the run command called on that device
# os_platform - OS information about the device
# groups - all the groups this device belongs to
# modules - all the attached modules on the device
# Asign_Id() - increments the id and asigns the device id as the new count
# Attach_Module() - attaches the given module to the device
# Change_Name() - Changes the name of the device
# Change_Type() - Changes the archetype of the device
# Delete_Device() - if the client is connected then disconnect it and remove the device from the devices dictionary
# Get_Run_Output() - returns the run_command_output of the device and resets it to None
# Set_Run_Output() - sets the run_command_output of the device

class Device():       #The device object to store device information
    devices = {}      #List of all devices created
    count = 0
    def __init__(self, client, name, archetype, id, serial, os_platform):
        self.client = client                     #Pass the socket object as client
        self.name = name                         #Set the name of the device(nickname)
        self.archetype = archetype               #Set the type of device that it is. will need to rework this for devices that have more than one sensor etc...           #
        if id == "-1":
            self.Asign_Id()
        else:
            self.id = id
        self.serial = serial
        Device.devices[self.id] = (self)       #Adds the device to the devices dictionar
        self.run_command_output = None         #Storage for run command output from the device
        self.os_platform = os_platform         #The devices platform type
        self.groups = []                       #All groups the device is part of
        self.modules = []                      #List of modules the device has attached

    def Asign_Id(self):
        Device.count += 1
        self.id = str(Device.count)
    
    def Attach_Module(self, module):
        self.modules.append(module)

    def __repr__(self) -> str:
        connected = "Connected"
        if self.client == None:
            connected = "Disconnected"
        return (f"id:{self.id} name:{self.name} type:{self.archetype} platform:{self.os_platform} status:{connected}")

    def Change_Name(self, new_name):
        self.name = new_name
    def Change_Type(self, new_type):
        self.archetype = new_type
    def Delete_Device(self):
        if self.client != None:
            self.client.close()
        del Device.devices[self.id]
    def Get_Runcommand_Output(self):
        output = self.run_command_output
        self.run_command_output = None
        return output
    def Set_Run_Output(self, data):
        self.run_command_output = data

#NOTE:Group Information
# groups - a dictionary of every group (key:group name | value:group object)
# devices - the list of device objects in the group
# name - the name of the group
# Add_Device - adds the device to the group
# Remove_Device - removes the device from the group
# Group_Delete - deletes the group from groups and removes the group from the device object as well
class Group():                                        #Groups used to logically organize devices
    groups = {}                                       #When a group is created we store it in the groups dictionary. The key is the group name.
    def __init__(self, name):
        self.devices = []                             #Store devices in this list to associate it with the group.
        self.name = name
        Group.groups[self.name] = self
    
    def __repr__(self) -> str:
        return (f"{self.devices}")
    
    def Add_Device(self, device):
        self.devices.append(device)
    
    def Remove_Device(self, device):
        self.devices.remove(device)
    
    def Group_Delete(name):
        group = Group.groups[name]
        for device in group.devices:
            device.groups.remove(group)
        del Group.groups[name]

#NOTE:Module Information
# name - the name of the module
# archetype - the type/description of the module
# frame - the last frame recieved from any attached camera
# Start_Camera_Feed() - returns the jpg encoded frame formatted for the Flask webpage
# Get_Camera_Frame() - returns the cameras current frame
# Set_Camera_Frame() - sets the frame variable to the frame passed in NOTE: This is used by the client
class Module():
    
    def __init__(self, name, archetype):
        self.name = name.lower()
        self.archetype = archetype.lower()
        self.frame = None

    def Start_Camera_Feed(self):
        while True:
            frame = self.frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def Get_Camera_Frame(self):
        return(self.frame)


    def Set_Camera_Frame(self, frame):
        self.frame = frame