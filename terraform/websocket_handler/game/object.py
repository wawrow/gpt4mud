class GameObject:
    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location

    def get_description(self):
        return self.description

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'location': self.location,
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls(data['name'], data['description'], None)
        return obj
    