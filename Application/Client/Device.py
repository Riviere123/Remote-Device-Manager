import platform
from DataFormatter import Protocol_Send
import numpy
import cv2
import pickle
import time
import threading
###Client side device object
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


#TODO add some sort of ID to diferentiate multiples of the same module type
class Module():
    def __init__(self, device, name, archetype):
        self.device = device
        self.name = name.lower()
        self.archetype = archetype.lower()
        self.frame = None
        self.start = False
    
    def Stop_Camera_Feed(self):
        return
    
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
