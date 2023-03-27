class Room:
    def __init__(self, name, description, connections):
        self.name = name
        self.description = description
        self.connections = connections

    def get_description(self):
        return self.description

    def get_connected_rooms(self):
        return self.connections
