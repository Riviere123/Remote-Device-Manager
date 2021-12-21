class Group():
    groups = []
    def __init__(self, name):
        self.name = name
        self.clients = []
        Group.groups.append(self)
    
    def __str__(self):
        return(f"{self.name}")