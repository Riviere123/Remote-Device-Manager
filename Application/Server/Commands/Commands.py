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
            return({"message":"Message sent"})
        else:
            return({"error":f"{device} is not connected"}) 
    def List():
        payload = []
        for id in Device.devices.keys():
            device = Device.devices[id]
            connected = "Connected"
            if device.client == None:
                connected = "Disconnected"
            payload.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
        return(payload)
    def Delete(device):
        device.Delete_Device()
        return({"message":f"{device.name} was deleted."})
    def Run(device, run_command):
        if device.client != None:
            Protocol_Send(device.client,run_command)
            return({"message":"Run Command Sent"})
        else:
            return({"message":f"{device} is not connected"}) 
    def Group_Create(group_name):
        group_name = group_name.lower() 
        if group_name in Group.groups.keys():
            return({"message":f"Group {group_name} already exists."})
        else:
            Group(group_name)
            return({"message":f"Group {group_name} created"})
    def Group_Add(group, device):
        if device in group.devices:
            return({"message":"Device already exists in that group."})
        else:
            group.Add_Device(device)
            device.groups.append(group)
            return({'message':f"Added {device.name} to {group.name}"})
    def Group_List():
        payload = {}
        for group in Group.groups:
            payload_devices = []
            for device in Group.groups[group].devices:
                connected = "Connected"
                if device.client == None:
                    connected = "Disconnected"
                payload_devices.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
            payload[group] = payload_devices
        return (payload)

    def Group_Delete(group_name):
        Group.Group_Delete(group_name)
        return({'message':f"{group_name} deleted"})
    def Group_Remove(group, device):
        group.Remove_Device(device)
        device.groups.remove(group)
        return({'message':f"{device.name} removed from {group.name}"})
    def Group_Send(group, message):
        for device in group.devices:
            Command.Send(device, message)
    def Group_Run(group, run_command):
        for device in group.devices:
            Command.Run(device,run_command)
#### HTTP HELPER COMMANDS
    def Get_Device_By_ID(id):
        device = Device.devices[id]
        connected = "Connected"
        if device.client == None:
            connected = "Disconnected"
        return({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
    def Get_Group_By_Name(group_name):
        group = Group.groups[group_name.lower()]
        payload_devices = []
        for device in group.devices:
            connected = "Connected"
            if device.client == None:
                connected = "Disconnected"
            payload_devices.append({"id":device.id, "name":device.name, "type":device.archetype, "status":connected})
        return(payload_devices)
