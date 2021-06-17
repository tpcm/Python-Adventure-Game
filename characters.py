from item1 import Weapon, Food
import random

class Characters:

    def __init__(self, name, hp, damage, gold):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.gold = gold



class Player(Characters):
    """
    This class is used to construct Player object to be used in the game.
    Initially the player has an empty inventory, max hp of 100 and 0 gold.

    """
    def __init__(self):
        """
            Constructor method
            Instantiate an empty inventory list to be used to carry items
            Instantiate hp with 100 point
            Instantiate gold value of 0
            Instantiate current_weapon variable to use to equip weapons
            
        """
        super().__init__(name="Player", hp=100, damage=5, gold=0)
        self.inventory = []
        self.max_weight = 50
        self.current_weapon = None


    def printInventory(self):
        """Method used to print items held in players inventory and the amount of gold."""
        if not self.inventory:
            print("Your inventory is currently empty")
            return False
        else:
            print("Items in Inventory:")
            for i in self.inventory:
                print(i.name)
            print(f"You have {self.gold} pieces")
            return True
    
    def addItem(self, item):
        """Method to add an item to the players inventory
            :param item: Item object 
            :return 0 if item is too heavy
        """
        # instantiate variable to accrue total weight already held and compare to max weight
        check_weight = 0
        # use for loop to add up total weight of inventory
        for i in self.inventory:
            check_weight += i.weight
        # check that adding the item won't take total weight over max weight
        if check_weight + item.weight <= self.max_weight:
            self.inventory.append(item)
        else:
            print("The item is too heavy")
            return 0

    def removeItem(self, item):
        """Method to remove an item from player inventory
            :param item: Item object
            :return: nothing
        """
        again = True
        while again == True:
            # Ask player if they want to remove item from inventory
            x = input(f"\nAre you sure you want to remove {item.name} from your inventory? ")
            # If player inputs yes
            if x.upper().strip() == "YES":
                # Remove item and inform player
                self.inventory.remove(item)
                print(f"\n{item.name} has been removed")
                again = False
                return True
            elif x.upper().strip() == "NO":
                again = False
                return False
            else:
                print("Sorry I didn't understand")

    def equipWeapon(self, weapon):
        """Method to allow player to equip the weapon of their choice
            :param weapon: weapon(item) object to be equiped
            :return: nothing
        """
        # instantiate a boolean to use as an escape clause
        equiped = False
        
        # Use while loop to allow the player to try again if they make a mistake
        while equiped == False:
            # Ask player if they would like to equip the weapon
            x = input(f"Would you like to equip the {weapon.name}?\n")
            # If player inputs yes
            if x.upper().strip() == "YES":
                # Set current weapon to weapon
                self.current_weapon = weapon
                # Inform player the weapon has been equiped
                print(f"\nYou have equiped the {self.current_weapon.name}")
                # Set equiped bool to True to end loop
                equiped = True
            # If player does not input yes    
            elif x.upper().strip() != "YES":                
                # Then ask if player wants to try again
                print(f"Are you sure you don't want to equip the {weapon.name}?")
                leave = input("Do you want to try again? ")
                # If player inputs no
                if leave.upper().strip() == "NO":
                    # Inform player that weapon is not equiped
                    print(f"Okay, the {weapon.name} will remain unequiped")
                    # Set equiped bool to True to end loop
                    equiped = True

    def playerEat(self):
        """A method used to heal the players hp with food items.
            :return: nothing
        """
        # Instantiate list with food names
        food_selection = ["BREAD", "MEAT", "POTATOES"]
        # Use list comprehension to instantiate and fill a list
        # with food items from player inventory if the food item is in food selection
        food_bag = [x for x in self.inventory if x.name.upper() in food_selection]
        # instantiate booleans to use as an escape clause
        again = False
        inside = None
        # use while loop to allow player to try again
        while again == False:
            # print list of food items to inform player of currently possessed food items
            print("The food items you currently possess in your inventory are: ")
            for food in food_bag:
                print(food.name)
            # ask player which food item they would like to heal themselves with
            y = input("Which food item would you like to consume? ")
            # for loop to iterate through whole inventory to check name equality
            for i in food_bag:
                # if statement to check whether player input is in inventory
                if i.name.upper() == y.upper().strip():
                    # Add item health value to player hp
                    self.hp += i.health
                    # Use if statement to cap hp at 100
                    if self.hp > 100:
                        self.hp = 100
                    # Remove item which has been used from player inventory
                    self.inventory.remove(i)
                    print(f"\nYour Hp is {self.hp}")
                    # Set inside to True
                    inside = True
                    break
            if inside == True:
                break
            # if y is not in the inventory, ask player if they would like to try again
            print(f"{y} is not in your inventory.")
            while again == False:
                leave = input("Would you like to try again? ")
                # If player doesn't input yes
                if leave.strip() == "no":
                    # Set again to True to end loop
                    again = True
                # If player inputs yes, break
                elif leave.strip() == "yes":
                    break
                # If player inputs whitspace, nothing etc loop
                elif leave.strip() != "yes":
                    print(f"Sorry I didn't understand\n")

    def attack(self, target):
        """A method to allow the player to attack enemies. The damage from the equiped weapon is taken off the enemies hp
           Three levels of damage are given, chosen at random
           :return: False if enemy hp drops below 0
        """
        # Allow player to attack with bare hands if no weapon equipped
        if self.current_weapon == None:
            print(f"You have no weapon equipped, so you attack with your bare hands")
            target.hp -= self.damage
        elif self.current_weapon != None:
            # random variable between 0,1,2 instantiated every time a method is called
            x = random.randint(0,2)
            # Use if loop to chose damage multiplier
            if x == 0:
                print(f"\nYou attack the {target.name} with your {self.current_weapon.name}, but you only scratch it") 
                # take the damage value of whichever weapon is equiped away from the enemies hp multiplied by 1
                target.hp -= self.current_weapon.damage
            elif x == 1:
                print(f"\nYou lunge at the {target.name}, striking a vital spot, critical hit!")
                # Damage is multiplied by 2
                target.hp -= self.current_weapon.damage * 2
            elif x == 2:
                print(f"\nYou strike with all your worth, slicing through the {target.name}'s defence, it's a fatal hit!")
                target.hp -= self.current_weapon.damage * 3
        
        # Print enemy's hp after every attack
        if target.hp > 0:
            print(f"The enemies health is now at {target.hp}")

        return True

class Trader(Characters):
    """This class is used to construct a Trader with whome the player may trade item with for gold.
        Initially the trader will have some items to trade with.
    """
    def __init__(self):
        """
            constructor method
            :param welcome: Boolean to describe whether player has already spoken to the trader, False if not, set to True after first encounter
            initialise a full inventory with differing quantities
        """
        super().__init__(name="Trader", hp=None, damage=None, gold=100)
        self.welcome = False
        self.createItems()

        self.inventory = [self.sword, self.axe, self.great_sword, self.battle_axe, self.bread, self.meat, self.potatoes]
    
    def createItems(self):
        """
            Sets up all weapon and food assets
            :return: None
        """
        self.sword = Weapon(name="Sword", value=15, weight=47, damage=10)
        self.axe = Weapon(name="Axe", value=12, weight=12, damage=8)
        self.great_sword = Weapon(name="GreatSword", value=25, weight=30, damage=18)
        self.battle_axe = Weapon(name="BattleAxe", value=35, weight=30, damage=25)
        self.bread = Food(name="Bread", value=3, weight=2, health=15)
        self.meat = Food(name="Meat", value=7, weight=4, health=20)
        self.potatoes = Food(name="Potatoes", value=7, weight=3, health=20)
    
    def welcomeSpeech(self):
        """A method to output a welcome speech"""
        print("Hello there, you look tired from your travels.")
        print("Why don't you have a look at my wares, there might be something you like?")

    def exitSpeech(self):
        """A method to output a leaving speech"""
        print("Farewell young traveller, safe journey!")

    def welcomeGift(self, customer):
        """A method used to gift the player with some food items at first encounter
            :param customer: must be a player class object to interact with 
        """
        print("Oh, isn't this the first time we've met?\nHere is a little welcome gift you should find helpful.")
        # instantiate meat item
        gift = Food(name="Meat", value=7, weight=4, health=20)
        # add meat item to player inventory
        customer.inventory.append(gift)
        print("There you go, you'll find the gift in your inventory.")

    def trade(self, customer):
        """
            A method to trade items for gold with a customer
            :param customer: Must be a player class object to interact with
        """
        # Instantiate a boolean to use in the while loop
        again = True
        while again == True:
            # Use try/except to handle index errors, repeat loop
            try:
                # Iterate through inventory and print items
                for i, stock in enumerate(self.inventory):
                    print(f"{i}: {stock.name}")
                # Take user input for item selection
                x = int(input("\nWhich item would you like to purchase? [ 9 to quit ] "))
                # If user inputs 9, break from loop
                if x == 9:
                    break
                # If player does not have enough gold, inform player
                # And ask if they would like to try again, if answer is not yes, break from loop 
                elif customer.gold < self.inventory[x].value:
                    print(f"\nYou do not have enough gold to purchase {self.inventory[x].name}")
                    z = input("\nWould you like to look again? ")
                    if z.upper().strip() != "YES":
                        break
                # If customer has the funds and selects correctly, add item to player inventory through player method addItem()
                else:
                    check = customer.addItem(self.inventory[x])
                    # If addItem() returns 0, inform player
                    if check == 0:
                        v = input("\nWould you like to try again? ")
                        if v.upper().strip() != "YES":
                            break
                    # Subtract item value from player gold
                    customer.gold -= self.inventory[x].value
                    print(f"\n{self.inventory[x].name} has been added to your inventory. You have {customer.gold} gold pieces left.")
                    # Remove item from trader inventory
                    self.inventory.remove(self.inventory[x])
                    k = input("Would that be all sir? ")
                    # ask if thats everything, if yes, break from loop
                    if k.upper().strip() == "YES":
                        again = False
            # Except index errors
            except IndexError as e:
                # Inform player of index error
                print(f"\n{e}")
                print("You need to input a number which corresponds to an item, or 9 to quit\n")
            # Except Value errors
            except ValueError as a:
                # Inform player of Value error
                print(f"\n{a}")
                print("You need to input an integer number\n")

class Enemy(Characters):
    """This is the base class for all enemies encountered"""
    def __init__(self, name, hp, damage, alive, gold):
        """
            constructor method
            :param name: Enemey name
            :param hp: The amount of hp the enemy has to start with
            :param damage: The amojunt of damage inflicted on player with each attack
            :param alive: Boolean to describe enemy hp, false if 0/below, True otherwise
            :param gold: The amount of gold the player will receive after defeating the enemy
        """
        super().__init__(name, hp, damage, gold)
        self.alive = alive
        
    
    def attackPlayer(self, player):
        """A method to allow enemies to attack the player. The enemies damage is taken away from players hp.
           Three levels of damage are given, chosen at random.
        """
        # random variable between 0,1,2 instantiated every time a method is called
        y = random.randint(0, 2)
        # Use if loop to chose damage multiplier
        if y == 0:
            print(f"\nThe {self.name} flails at you and barely hits!")
            # Take enemy damge integer divided by 2 away from player hp
            player.hp -= self.damage // 2
        elif y == 1:
            print(f"\nThe {self.name} launches itself at you and lands a clean hit!")
            # Take enemy damage multiplied by 1 away from player hp
            player.hp -= self.damage
        elif y == 2:
            print(f"\nThe {self.name} attacks, catching you by surprise, and lands a critical hit!")
            # Take enemy damage multiplied by 1.5 away from player hp
            player.hp -= self.damage * 1.5
        # Print player hp after every attack
        if player.hp > 0:
            print(f"You now have {player.hp} hp\n")
        
        return True