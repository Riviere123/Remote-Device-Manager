class Device:
    this_device = None
    def __init__(self, name, archetype):
        self.name = name
        self.archetype = archetype
        Device.this_device = self
        self.server = None
    def __repr__(self) -> str:
        return(f"name:{self.name} type:{self.archetype}")