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
        self.player = Player('Player', self.rooms['start'])
        self.objects = [
            GameObject('key', 'A small key.', self.rooms['start'])
        ]
        self.npcs = [
            NPC('NPC', 'A friendly NPC.', self.rooms['end'])
        ]

    def process_command(self, command):
        if command == 'look':
            return self.player.current_room.get_description()
        elif command in ['north', 'south', 'east', 'west']:
            return self.player.move(command, self.rooms)
        elif command == 'inventory':
            return self.player.get_inventory()
        elif command == 'pick up key':
            return self.player.pick_up_object(self.objects[0])
        elif command == 'talk to NPC':
            return self.npcs[0].interact()
        else:
            return 'Invalid command.'
