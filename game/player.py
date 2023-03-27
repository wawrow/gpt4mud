class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.inventory = []

    def move(self, direction, rooms):
        if direction in self.current_room.connections:
            self.current_room = rooms[self.current_room.connections[direction]]
            return self.current_room.get_description()
        else:
            return "You can't go that way."

    def get_inventory(self):
        if not self.inventory:
            return 'Your inventory is empty.'
        return ', '.join([obj.name for obj in self.inventory])

    def pick_up_object(self, obj):
        if obj.location == self.current_room:
            self.inventory.append(obj)
            obj.location = None
            return f'You picked up {obj.name}.'
        else:
            return "You can't find that object here."
