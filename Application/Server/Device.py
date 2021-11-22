class Device():       #The device object to store device information
    devices = {}      #List of all devices created
    count = 0
    def __init__(self, client, name, archetype, id):
        self.client = client                     #Pass the socket object as client
        self.name = name                         #Set the name of the device(nickname)
        self.archetype = archetype               #Set the type of device that it is. will need to rework this for devices that have more than one sensor etc...           #
        if id == "-1":
            self.Asign_Id()
        else:
            self.id = id
        Device.devices[self.id] = (self)       #Adds the device to the devices dictionary
        self.groups = []

    def Asign_Id(self):
        Device.count += 1
        self.id = str(Device.count)

    def __repr__(self) -> str:
        connected = "Connected"
        if self.client == None:
            connected = "Disconnected"
        return (f"ID:{self.id} Name:{self.name} archetype:{self.archetype} - {connected}")

    ###Changes the devices name and changes the key in the devices dictionary
    def Change_Name(self, new_name):
        self.name = new_name
    def Change_Type(self, new_type):
        self.archetype = new_type
    def Delete_Device(self):
        if self.client != None:
            self.client.close()
        del Device.devices[self.id]

class Group():                                        #Groups used to logically organize devices
    groups = {}                                       #When a group is created we store it in the groups dictionary. The key is the group name.
    def __init__(self, name):
        self.devices = []                             #Store devices in this list to associate it with the group.
        self.name = name
        Group.groups[self.name] = self
    
    def __repr__(self) -> str:
        return (f"Group:{self.name} Devices:{self.devices}")
    
    def Add_Device(self, device):
        self.devices.append(device)
    
    def Remove_Device(self, device):
        self.devices.remove(device)
    
    def Group_Delete(name):
        del Group.groups[name]

