import platform
from DataFormatter import Protocol_Send
import cv2
import pickle
import threading
###Client side device object
#NOTE:Device Information
# name - name given to the device
# Archetype - The devices type/description
# Server - The socket stream to the server
# id - The devices id this is given by the server and is used by the server
# serial - Unique serial number generated for each device. Used to to recognize previously connected devices. Server stores the serial number in there device object.
# os_platform - the os information for the device
# modules - List of modules that are connected to the device

#TODO Make creation of modules easy - Have a module install wizard that walks the user through connecting module to there local device
# Make modules recognize devices IE. When user chooses camera, recognize if it's webcam, pi cam, etc. and setup accordingly
class Device:
    this_device = None
    def __init__(self, name, archetype, serial):
        self.name = name
        self.archetype = archetype
        self.server = None                         
        self.id = "-1"
        self.serial = serial
        Device.this_device = self
        self.os_platform = platform.platform()
        self.modules = []
    def __repr__(self) -> str:
        return(f"id:{self.id} name:{self.name} type:{self.archetype} platform:{self.os_platform}, modules:{self.modules}")
    
    def Attach_Module(self, module):
        self.modules.append(module)
    def Send_Module_data(self):
        for module in self.modules:
            Protocol_Send(self.server, f"attach mod {module.name} {module.archetype}")


#TODO add a way to diferentiate two of the same archetypes of models.
#NOTE: Module information
# device - references this device that it's attached to
# name - the name of the module
# archetype - the type/description of the module
# frame - stores the current frame of the camera when the camera is started
# start - designates wether the module is active or not
# _Camera() - the method that is called from Start_Camera which gets the frame data and sends the set frame command to the server with the data
# Start_Camera() - starts the _Camera() in a new thread freeing the terminal to input more commands
# Stop_Camera() - Changes the start variable to False turning off the module #NOTE: Think about changing to a more generic name to suite all modules
class Module():
    def __init__(self, device, name, archetype):
        self.device = device
        self.name = name.lower()
        self.archetype = archetype.lower()
        self.frame = None
        self.start = False
    
    def _Camera(self):
        self.start = True
        camera =cv2.VideoCapture(0)
        while self.start:
            success, frame = camera.read()
            if not success:
                break
            else:
                data = pickle.dumps(frame)
                
                Protocol_Send(self.device.server, f"set frame {data}")
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        camera.release()
        cv2.destroyAllWindows()
    
    def Start_Camera(self):
        camera_thread = threading.Thread(target=self._Camera)
        camera_thread.start()
    
    def Stop_Camera(self):
        self.start = False
