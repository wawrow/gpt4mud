from game.npc import NPC, Quest

class OldManQuest(Quest):
    def __init__(self):
        super().__init__(
            name="Find the Enchanted Artifact",
            description="The old man asks you to retrieve a hidden enchanted artifact.",
            steps=[
                "Talk to the innkeeper at the tavern.",
                "Talk to the shopkeeper at the shop.",
                "Talk to the blacksmith at the blacksmith's workshop.",
                "Return to the old man with the information you've gathered."
            ],
            rewards=["Enchanted Artifact"],
            complete=False
        )

    def complete(self, player):
        super().complete(player)
        enchanted_artifact = self.game.get_object("enchanted_artifact")
        enchanted_artifact.location = player.id
        self.game.send_message(player.id, "The old man hands you the enchanted artifact as a reward.")
        self.game.send_message(player.id, "As you take the artifact, you sense there are more adventures to come...")

npc = NPC(
    name="Old Man",
    description="An old man with a mysterious aura. He seems to know something about the enchanted artifact.",
    location="town_square"
)

npc.add_quest(OldManQuest())
