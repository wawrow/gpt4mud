class NPC:
    def __init__(self, name, description, location, game=None):
        self.name = name
        self.description = description
        self.location = location
        self.quests = []
        self.game = game

    def get_description(self):
        return self.description

    def interact(self):
        return "Hello, I'm just a friendly NPC!"

    def add_quest(self, quest):
        """
        Adds a quest to the NPC's list of quests.

        :param quest: An instance of the Quest class.
        """
        self.quests.append(quest)
        quest.npc = self
        quest.game = self.game

class Quest:
    def __init__(self, name, description, steps, rewards, complete=False):
        self.name = name
        self.description = description
        self.steps = steps
        self.rewards = rewards
        self.complete = complete

    def is_complete(self):
        return self.complete

    def complete(self, player):
        self.complete = True
        for reward in self.rewards:
            player.inventory.append(reward)
