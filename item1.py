class Item:
    """This is a base class for all items such as weapons and food"""
    def __init__(self, name, value, weight):
        """
            constructor method
            :param name: Item name
            :param value: the items value
            :param weight: the items weight
        """
        
        self.name = name
        self.value = value
        self.weight = weight

class Weapon(Item):
    """A base class for weapon type object used to attack enemies with Item as a super class"""
    def __init__(self, name, value, weight, damage):
        """
            constructor method
            :param name: Item name
            :param value: the items value
            :param weight: the items weight
            :param damage: integer value of how much damage the weapon inflicts 
        """
        super().__init__(name, value, weight)
        self.damage = damage

class Food(Item):
    """A super class for food type object used to heal player"""
    def __init__(self, name, value, weight, health):
        """
            constructor method
            :param name: Item name
            :param value: the items value
            :param weight: the items weight
            :param health: integer value of how much health the item provides to the player 
        """
        super().__init__(name, value, weight)
        self.health = health