from game.room import Room

room = Room(
    name="Town Square",
    description="You find yourself in a quaint town square, surrounded by small buildings nestled between the mountains where two rivers meet."
)

room.add_exit("north", "tavern")
room.add_exit("east", "shop")
room.add_exit("south", "blacksmith")
