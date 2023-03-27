from game.room import Room
from game.player import Player
from game.object import GameObject
from game.npc import NPC

class Game:
    def __init__(self):
        self.rooms = {
            'start': Room('Start Room', 'You are in the starting room.', {'east': 'end'}),
            'end': Room('End Room', 'You are in the ending room.', {'west': 'start'})
        }
        self.objects = [
            GameObject('key', 'A small key.', self.rooms['start'])
        ]
        self.npcs = [
            NPC('NPC', 'A friendly NPC.', self.rooms['end'])
        ]
        self.players = {}

    def add_player(self, sid):
        self.players[sid] = Player(sid, self.rooms['start'])
        return self.players[sid].current_room.get_full_description(self.players, self.objects, self.npcs)

    def remove_player(self, sid):
        if sid in self.players:
            del self.players[sid]

    def process_command(self, sid, command):
        player = self.players[sid]
        if command == 'look':
            return player.current_room.get_full_description(self.players, self.objects, self.npcs)
        elif command in ['north', 'south', 'east', 'west']:
            return player.move(command, self.rooms)
        elif command == 'inventory':
            return player.get_inventory()
        elif command == 'pick up key':
            return player.pick_up_object(self.objects[0])
        elif command == 'talk to NPC':
            return self.npcs[0].interact()
        else:
            return 'Invalid command.'
