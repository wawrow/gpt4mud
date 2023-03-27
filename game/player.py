class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.inventory = []

    def move(self, direction):
        # Move player to the specified direction
        pass

    def pick_up_object(self, obj):
        # Pick up an object and add it to the inventory
        pass

    def drop_object(self, obj):
        # Drop an object from the inventory
        pass
