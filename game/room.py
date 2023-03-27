class Room:
    def __init__(self, name, description, connections):
        self.name = name
        self.description = description
        self.connections = connections

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