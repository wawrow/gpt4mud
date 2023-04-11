class Room:
    def __init__(self, name, description, connections=None):
        self.name = name
        self.description = description
        self.connections = {} if connections is None else connections

    def add_exit(self, direction, target_room_id):
        """
        Adds an exit to the room.

        :param direction: A string representing the direction of the exit (e.g. "north").
        :param target_room_id: The ID of the room that the exit leads to.
        """
        self.connections[direction] = target_room_id

    def get_description(self):
        return self.description

    def get_connected_rooms(self):
        return self.connections

    def get_full_description(self, players, objects, npcs):
        description = f"{self.name}\n{self.description}\n"
        
        exits = ', '.join([direction.capitalize() for direction, room_name in self.connections.items() if room_name])
        description += f"Exits: {exits}\n"

        room_objects = [obj for obj in objects if obj.location == self]
        if room_objects:
            description += "Objects:\n"
            for obj in room_objects:
                description += f"  - {obj.name}\n"

        room_npcs = [npc for npc in npcs if npc.location == self]
        if room_npcs:
            description += "NPCs:\n"
            for npc in room_npcs:
                description += f"  - {npc.name}\n"

        room_players = [player for player in players.values() if player.current_room == self]
        if room_players:
            description += "Players:\n"
            for player in room_players:
                description += f"  - {player.name}\n"

        return description.strip()

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "connections": {direction: room.lower() if isinstance(room, str) else room.name.lower() for direction, room in self.connections.items()},
        }

    @classmethod
    def from_dict(cls, data, game):
        room = cls(data["name"], data["description"])

        # Rebuild room connections
        for direction, connected_room_id in data["connections"].items():
            connected_room = game.rooms[connected_room_id]
            room.add_exit(direction, connected_room)

        return room
