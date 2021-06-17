"""
    Create a room described "description". Initially, it has
    no exits. 'description' is something like 'kitchen' or
    'an open court yard'
"""

class Room:

    def __init__(self, description, enemy, completed=False):
        """
            Constructor method
            :param description: text description for this room
            :param enemy: Assigns the enemy for the room if there is one
            :param completed: Boolean to describe whether room has been completed        
        """
        self.description = description
        self.enemy = enemy
        self.completed = completed
        self.exits = {}     # Dictionary
        

    def setExit(self, direction, neighbour):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room)
        :param direction: The direction leading out of this room
        :param neighbour: The room that this direction takes you to
        :return: None
        """
        self.exits[direction] = neighbour

    def getShortDescription(self):
        """
            Fetch a short text description
        :return: text description
        """
        return self.description

    def getLongDescription(self):
        """
            Fetch a longer description including available exits
        :return: text description
        """
        return f'Location: {self.description} \nExits: {self.getExits()} '

    def getExits(self):
        """
            Fetch all available exits as a list
        :return: list of all available exits
        """
        allExits = self.exits.keys()
        return list(allExits)

    def getExit(self, direction):
        """
            Fetch an exit in a specified direction
        :param direction: The direction that the player wishes to travel
        :return: Room object that this direction leads to, None if one does not exist
        """
        if direction in self.exits:
            return self.exits[direction]
        else:
            return None
