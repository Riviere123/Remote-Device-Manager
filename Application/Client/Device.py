class Device:
    this_device = None
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
        self.server = None
        self.id = "-1"
        Device.this_device = self
    def __repr__(self) -> str:
        return(f"id:{self.id} name:{self.name} type:{self.archetype}")