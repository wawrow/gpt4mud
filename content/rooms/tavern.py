from game.room import Room

room = Room(
    name="Tavern",
    description="You enter a cozy tavern. Locals are gathered around tables, chatting and enjoying their drinks."
)

room.add_exit("south", "town_square")
