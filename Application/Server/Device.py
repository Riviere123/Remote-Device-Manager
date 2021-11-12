class Device():       #The device object to store device information and eventually functionality
    devices = {}      #List of all devices created

    def __init__(self, client, name, archetype):
        self.client = client              #Pass the socket object as client
        self.name = name                  #Set the name of the device(nickname)
        self.archetype = archetype        #Set the type of device that it is. will need to rework this for devices that have more than one sensor etc...           #
        Device.devices[self.name] = (self)       #Adds the device to the devices dictionary
    
    def __repr__(self) -> str:
        return (f"Name: {self.name} archetype: {self.archetype} Address: {self.client}")

    ###Changes the devices name and changes the key in the devices dictionary
    def Change_Name(self, new_name):
        del Device.devices[self.name]
        self.name = new_name
        Device.devices[new_name] = self
        