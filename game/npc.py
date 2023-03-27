class NPC:
    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location

    def get_description(self):
        return self.description

    def interact(self, player):
        # Interaction between player and NPC
        pass
