from game.room import Room

room = Room(
    name="Blacksmith",
    description="You arrive at the blacksmith's workshop. The sound of metal striking metal fills the air as the blacksmith works on a new piece of equipment."
)

room.add_exit("north", "town_square")
