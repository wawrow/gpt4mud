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
        description = self.get_description()

        exits = ', '.join(self.connections.keys())
        description += f'\nExits: {exits}'

        items = [obj for obj in objects if obj.location == self]
        if items:
            items_str = ', '.join([item.name for item in items])
            description += f'\nItems: {items_str}'

        room_npcs = [npc for npc in npcs if npc.location == self]
        if room_npcs:
            npcs_str = ', '.join([npc.name for npc in room_npcs])
            description += f'\nNPCs: {npcs_str}'

        room_players = [player for player in players.values() if player.current_room == self]
        if room_players:
            players_str = ', '.join([player.name for player in room_players])
            description += f'\nPlayers: {players_str}'

        return description
