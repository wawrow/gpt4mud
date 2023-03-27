import os
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from game.room import Room
from game.player import Player
from game.object import GameObject
from game.npc import NPC
from .name_generator import generate_name


class ContentEventHandler(FileSystemEventHandler):
    def __init__(self, game):
        self.game = game

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'Reloading content: {event.src_path}')
            self.game.load_content()


class Game:
    def __init__(self):
        self.rooms = {}
        self.objects = []
        self.npcs = []
        self.players = {}

        self.load_content()
        self.start_watching_content()

    def load_content(self):
        self.load_rooms()
        self.load_objects()
        self.load_npcs()

    def start_watching_content(self):
        event_handler = ContentEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, 'content', recursive=True)
        observer.start()

    def load_rooms(self):
        rooms_path = 'content/rooms'
        for file_name in os.listdir(rooms_path):
            if file_name.endswith('.py'):
                module_name = f'content.rooms.{file_name[:-3]}'
                module = importlib.import_module(module_name)
                room = getattr(module, 'room', None)
                if room:
                    self.rooms[room.name.lower()] = room

    def load_objects(self):
        objects_path = 'content/objects'
        for file_name in os.listdir(objects_path):
            if file_name.endswith('.py'):
                module_name = f'content.objects.{file_name[:-3]}'
                module = importlib.import_module(module_name)
                obj = getattr(module, 'obj', None)
                if obj:
                    self.objects.append(obj)
                    room_name = obj.location and obj.location.lower()
                    if room_name in self.rooms:
                        obj.location = self.rooms[room_name]

    def load_npcs(self):
        npcs_path = 'content/npcs'
        for file_name in os.listdir(npcs_path):
            if file_name.endswith('.py'):
                module_name = f'content.npcs.{file_name[:-3]}'
                module = importlib.import_module(module_name)
                npc = getattr(module, 'npc', None)
                if npc:
                    self.npcs.append(npc)
                    room_name = npc.location.lower()
                    if room_name in self.rooms:
                        npc.location = self.rooms[room_name]
                    npc.game = self

    def add_player(self, sid):
        name = generate_name()
        self.players[sid] = Player(sid, name, self.rooms['start room'])
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
        elif command.startswith('pick up '):
            object_name = command[8:]
            obj = next((obj for obj in self.objects if obj.name.lower() == object_name.lower()), None)
            if obj:
                return player.pick_up_object(obj)
            else:
                return f"You can't find {object_name} here."
        elif command.startswith('talk to '):
            npc_name = command[8:]
            npc = next((npc for npc in self.npcs if npc.name.lower() == npc_name.lower()), None)
            if npc:
                return npc.interact()
            else:
                return f"You can't find {npc_name} here."
        else:
            return 'Invalid command.'
