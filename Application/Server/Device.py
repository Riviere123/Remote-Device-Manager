class Device():       #The device object to store device information and eventually functionality
    devices = []      #List of all devices created

    def __init__(self, client, name, archetype):
        self.client = client              #Pass the client reference to the device object
        self.name = name                  #Set the name of the device(nickname)
        self.archetype = archetype        #Set the type of device that it is. will need to rework this for devices that have more than one sensor etc...           #
        Device.devices.append(self)       #Adds the device to the devices list
    
    def __repr__(self) -> str:
        return (f"Name: {self.name} archetype: {self.archetype} Address: {self.client.address}")