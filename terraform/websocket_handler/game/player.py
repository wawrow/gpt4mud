from game.object import GameObject


class Player:
    def __init__(self, sid, name, current_room):
        self.sid = sid
        self.name = name
        self.current_room = current_room
        self.inventory = []

    def move(self, direction, rooms):
        if direction in self.current_room.connections:
            self.current_room = self.current_room.connections[direction]
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
        
    def to_dict(self):
        return {
            'sid': self.sid,
            'name': self.name,
            'current_room': self.current_room.name.lower(),
            'inventory': [obj.name for obj in self.inventory]
        }
    
    @classmethod
    def from_dict(cls, data, game):
        player = cls(data['sid'], data['name'], game.rooms[data['current_room'].lower()])
        player.inventory = [GameObject(name) for name in data['inventory']]
        return player
    