from Device import Device, Group
from DataFormatter import Protocol_Receive, Protocol_Send
class Command():
################## Commands called from a client ############################
    def Set_Name(device, new_name):
        if new_name in Device.devices.keys():
            Protocol_Send(device.client, "Error: That name is already in use.")
            return("Error: Device name is already in use.")
        else:                                            
            device.Change_Name(new_name)
            return(f"{device.name}'s name has been changed to {new_name}")  
    def Set_Type(device, new_type):                      
        device.Change_Type(new_type)
        return(f"{device.name}'s device type changed to {new_type}")

################## Commands called from server ############################
#TODO I take out device and group passins because they will not work with HTTP calls only strings!
    def Send(device, message):
        if device.client != None:
            Protocol_Send(device.client, message)
            return("Message sent")
        else:
            return(f"{device} is not connected") 
    def List():
        output = {}
        lst = Device.devices
        for x in lst:
            connected = "Connected"
            if lst[x].client == None:
                connected = "Disconnected"
            output[x] = {"name":lst[x].name, "type":lst[x].archetype, "status":connected}
        return(output)
    def Delete(device):
        device.Delete_Device()
    def Run(device, run_command):
        if device.client != None:
            Protocol_Send(device.client,run_command)
            return("Run Command Sent")
        else:
            return(f"{device} is not connected") 
    def Group_Create(group_name): 
        if group_name in Group.groups.keys():
            return(f"Group {group_name} already exists.")
        else:
            Group(group_name)
            return(f"Group {group_name} created")
    def Group_Add(group, device):
        if device in group.devices:
            return("Device already exists in that group.")
        else:
            group.Add_Device(device)
            device.groups.append(group)
            return(f"Added {device.name} to {group.name}")
    def Group_List():
        return (Group.groups)
    def Group_Delete(group_name):
        Group.Group_Delete(group_name)
        return(f"{group_name} deleted")
    def Group_Remove(group, device):
        group.Remove_Device(device)
        device.groups.remove(group)
        return(f"{device.name} removed from {group.name}")
    def Group_Send(group, message):
        for device in group.devices:
            Command.Send(device, message)
    def Group_Run(group, run_command):
        for device in group.devices:
            Command.Run(device,run_command)
        
