from game.room import Room

room = Room(
    name="Shop",
    description="You step into a small shop filled with various items and trinkets for sale."
)

room.add_exit("west", "town_square")
