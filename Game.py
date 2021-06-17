from Room import Room
from TextUI import TextUI
from characters import Player, Trader, Enemy
from item1 import Weapon, Food
import time
import random
import logging

"""
    This class is the main class of the "Adventure World" application. 
    'Adventure World' is a very simple, text based adventure game.  Users 
    can walk around some scenery. That's all. It should really be extended 
    to make it more interesting!
    
    To play this game, create an instance of this class and call the "play"
    method.

    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game.  It also evaluates and
    executes the commands that the parser returns.
    
    This game is adapted from the 'World of Zuul' by Michael Kolling
    and David J. Barnes. The original was written in Java and has been
    simplified and converted to Python by Kingsley Sage
"""
class Game:

    def __init__(self):
        """
        Initialises the game
        """
        self.player = Player()
        self.createNPC()
        self.dagger = Weapon(name="Dagger", value=5, weight=5, damage=5)
        self.hallroom_bread = Food(name="Bread", value=3, weight=2, health=15)
        self.createRooms()
        self.currentRoom = self.outside
        self.textUI = TextUI()
        logging.basicConfig(filename="TextUiUserInput.log", level=logging.INFO)

    def createNPC(self):
        """
            Sets up all enemy and trader assets
            :return: None
        """
        self.corridor_goblin = Enemy(name="Corridor Goblin", hp=20, damage=10, alive=True, gold=30)
        self.baths_bandit = Enemy(name="Bandit", hp=40, damage=18, alive=True, gold=30)
        self.bedroom_goblin = Enemy(name="Bedroom Goblin", hp=40, damage=18, alive=True, gold=30)
        self.study_wizard = Enemy(name="Wizard", hp=80, damage=22, alive=True, gold=50)
        self.warlord = Enemy(name="Warlord", hp=120, damage=30, alive=True, gold=None)
        self.lounge_trader = Trader()

    def createRooms(self):

        """
            Sets up all room assets
            :return: None
        """
        # Instantiate all rooms to be used
        self.outside = Room("\nYou are outside the dungeon, in front of you is the entrance, a door so tall you ask yourself what could possibly require a door so big?", enemy=None, completed=None)
        self.lobby = Room("\nThrough the towering doors, you enter what must be a lobby. The room is fairly empty, there appears to be a sign in the centre of the room.", enemy=None)
        self.corridor = Room("\nYou enter a long and narrow corridor, with walls covered in blood and gore, a warning to unprepared travellers.", enemy=self.corridor_goblin)
        self.hallroom = Room("\nThis room has great long table, with deep gouges throughout, and around the table are dusty old wooden chairs, half of which are a broken mess.\nThe shadows seem to be moving...", enemy=None,)
        self.lounge = Room("\nYou enter what appers to be a lounge, with dusty, worn cushioned seats. By the fireplace appears to be another person, with wares to be inspected.", enemy=None)
        self.baths = Room("\nThis room is full of steam, with large basins filled with hot water. It's not just water occupying the basins however... ", enemy=self.baths_bandit)
        self.bedroom = Room("\nA large bed seems to be the focal point of this otherwise empty room. A room whose wall are stained with blood and smeared with some sort of black substance. Crawling out from under the bed come a group of goblins", enemy=self.bedroom_goblin)
        self.study = Room("\nYou walk into a room filled with books and paper with sketches on. You take a closer look... the writting and sketches appear to account for sick experiments done on living people. This must be the Warlocks study.", enemy=self.study_wizard)
        self.throneroom = Room("\nAfter descending to the very depths of the dungeon, you walk into the throneroom. And sat upon his throne, as if awaiting your arrival, is the Dungeon Lord himself,\nwhose ghastly appearence chills you to your core. I hope you're ready traveller...", enemy=self.warlord)
        # first room is outside, enter to start game
        self.outside.setExit("inside", self.lobby)
        # next three rooms are inline
        self.lobby.setExit("south", self.corridor)
        self.corridor.setExit("west", self.hallroom)
        # rooms 5-6 are on middle floor, descend to enter lounge
        # the lounge is at the centre of the middle floor
        # only way to enter other rooms is through the lounge
        self.hallroom.setExit("down", self.lounge)
        self.lounge.setExit("east", self.baths)
        self.lounge.setExit("west", self.bedroom)
        self.baths.setExit("west", self.lounge)
        self.bedroom.setExit("east", self.lounge)
        # Must descend from middle floor to the bottom floor
        self.lounge.setExit("down", self.study)
        self.study.setExit("south", self.throneroom)
        
    def play(self):
        """
            The main play loop
        :return: None
        """
        self.printWelcome()
        finished = False
        while (finished == False):
            command = self.textUI.getCommand()      # Returns a 2-tuple
            finished = self.processCommand(command)

        print("\nThank you for playing!")

    def printWelcome(self):
        """
            Displays a welcome message at timed intervals
        :return:
        """
        self.textUI.printtoTextUI("\nHello traveller, I'm glad to see you want to attempt what others have failed")
        self.textUI.printtoTextUI("Let me tell you what the task you are about to attempt entails")
        time.sleep(4)
        self.textUI.printtoTextUI("\nYou must advance through the dungeon, moving through each room")
        self.textUI.printtoTextUI("Picking up any items offered and defeating all enemies that you come accross")
        time.sleep(4)
        self.textUI.printtoTextUI("At the very bottom of the dungeon awaits the Dungeon Lord, the tyrant who rules this region")
        time.sleep(4)
        self.textUI.printtoTextUI("It is your duty to defeat this evil creature and free the land from his evil reign")
        time.sleep(4)
        self.textUI.printtoTextUI("\nI will accompany you on your journey, just think of me as your invisible companion")
        time.sleep(4)
        self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')
        time.sleep(4)
        self.textUI.printtoTextUI("\nTo start if you want to use an exit, input 'go' followed by the direction of your choice")
        time.sleep(4)
        self.textUI.printtoTextUI("For example, 'go west' will take you to the room to the west of you")
        time.sleep(4)
        self.textUI.printtoTextUI("\nIf you come accross an enemy, inputting attack will trigger a combat sequence between you and the enemy")
        self.textUI.printtoTextUI("You must kill the rooms enemy and pick up any items in order to complete the room and move on")
        time.sleep(4)
        self.textUI.printtoTextUI("\nIf you would like to see the items you have in your inventory, input 'inventory'")
        time.sleep(4)
        self.textUI.printtoTextUI(f"You can only carry up to {self.player.max_weight}kg though, so be mindful of what you carry")
        time.sleep(4)
        self.textUI.printtoTextUI("\nThe commands, eat, trade, equip and remove do exactly that")
        time.sleep(3)
        self.textUI.printtoTextUI("\n\nWelcome to the Dungeon Run, Let us now begin, companion\n\n")
        time.sleep(3)
        self.textUI.printtoTextUI(self.currentRoom.getLongDescription())
        time.sleep(4)
        self.textUI.printtoTextUI("What will you do?")
        
    def showCommandWords(self):
        """
            Show a list of available commands
        :return: None
        """
        return ['help', 'go', 'quit', 'attack', 'inventory', 'eat', 'trade', 'equip', 'remove']

    def processCommand(self, command):
        """
            Process a command from the TextUI
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = command
        if commandWord != None:
            commandWord = commandWord.upper()

        wantToQuit = False
        
        if commandWord == "HELP":
            self.doPrintHelp()

        elif commandWord == "GO":
            # If player tries to leave the room before completing it
            if self.currentRoom.completed == False:
                # Inform player the room needs to be completed
                self.textUI.printtoTextUI("You have not completed the room.")
            # Only allow player to descend to the last floor if the middle floor has been entirely completed
            # If the current room is the lounge and the second command word is down
            elif self.currentRoom == self.lounge and secondWord.upper() == "DOWN":
                # If the baths or bedroom have not been completed
                if self.baths.completed != True or self.bedroom.completed != True:
                    # Inform player baths and bedroom need to be completed
                    self.textUI.printtoTextUI("You must clear the other two rooms first before descending to the lower level")
                # Else call doGoCommand() method
                else:
                    self.doGoCommand(secondWord)
            else:
                self.doGoCommand(secondWord)
        elif commandWord == "QUIT":
            wantToQuit = True

        elif commandWord == "ATTACK":
            # If player inputs attack with no enemies present, inform player there are no enemies prersent
            # Get another command
            if self.currentRoom.enemy == None or self.currentRoom.enemy.alive == False:
                self.textUI.printtoTextUI("There are no enemies to attack in this room")
                self.textUI.printtoTextUI("What will you do?")
            
            else:
                # If there is an enemy present in the current room, call doAttack method
                x = self.doAttack()
                # If self.doAttack returns 1 
                if x == 1:
                    # After completing doAttack() method, set currentRoom.completed to True
                    # This allows the player to leave
                    self.currentRoom.completed = True
                    # Print specific messages for certain rooms after calling doAttack() method
                    if self.currentRoom == self.baths:
                        time.sleep(2)
                        self.textUI.printtoTextUI("\nThat was quick work, and you have succeeded in scaring the rest of them off")
                        self.textUI.printtoTextUI("Let us still move quickly, in case they change their mind")
                    # If in the last room, throneroom
                    elif self.currentRoom == self.throneroom:
                        time.sleep(2)
                        self.textUI.printtoTextUI("\nCompanion, you have vanquished the Demon Lord")
                        self.textUI.printtoTextUI("This land owes you a debt of gratitude, Farewell!")
                        # set wantToQuit to True to end game
                        wantToQuit = True
                    else:
                        self.textUI.printtoTextUI("\nWell done companion, what is our next step?")
                # If self.doAttack reutrns 0, end the game
                elif x == 0:
                    wantToQuit = True
                    
        elif commandWord == "INVENTORY":
            # Call player method to list contents of inventory
            self.player.printInventory()

        elif commandWord == "EAT":
            self.doEat()

        elif commandWord == "TRADE":
            # If player is not in lounge inform player trading cannot take place
            if self.currentRoom != self.lounge:
                self.textUI.printtoTextUI("There is no trader present to trade with")
            # If current room is lounge
            else:
                # Call doTrade() method
                self.doTrade()

        elif commandWord == "EQUIP":
            # call doEquip() method
            self.doEquip()
                

        elif commandWord == "REMOVE":
            removal = self.doRemove()
            if removal == False:
                wantToQuit = False

        else:
            # Unknown command ...
            self.textUI.printtoTextUI("Don't know what you mean")
        # Print the current room's exits and
        
        if wantToQuit != True:
            self.textUI.printtoTextUI(f"\nExits: {self.currentRoom.getExits()}")
            self.textUI.printtoTextUI(self.showCommandWords())

        # Logs the user input in the log file created in the constructor
        logging.info(command)
        return wantToQuit

    def doPrintHelp(self):
        """
            Display some useful help text
        :return: None
        """
        self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')
        self.textUI.printtoTextUI("Remember if there is a creature present, you must attack and defeat it to move on")

    def doGoCommand(self, secondWord):
        """
            Performs the GO command
        :param secondWord: the direction the player wishes to travel in
        :return: None
        """

        if secondWord == None:
            # Missing second word ...
            self.textUI.printtoTextUI("Go where?")
            return


        nextRoom = self.currentRoom.getExit(secondWord)
        if nextRoom == None:
            self.textUI.printtoTextUI("There is no door in that direction!")
        # If the player tries to go back into the baths
        elif self.currentRoom == self.lounge and nextRoom == self.baths and self.baths.completed == True:
            self.textUI.printtoTextUI("You have already completed this room, it would be a waste of time to go back")
            return
        # If the player tries to go back into the bedroom they are blocked
        elif self.currentRoom == self.lounge and nextRoom == self.bedroom and self.bedroom.completed == True:
            self.textUI.printtoTextUI("You have already completed this room, it would be a waste of time to go back")
            return
        else:
            self.currentRoom = nextRoom
            self.textUI.printtoTextUI(self.currentRoom.getLongDescription())

    
        # Use if loop to set into motion events that happen on the first instance a room is entered
        if self.currentRoom == self.lobby:
            time.sleep(2)
            if self.currentRoom.completed != True:
                # Prints further description of what takes place in the room
                self.textUI.printtoTextUI("\nAs you walk around the lobby you find something on the floor.")
                self.textUI.printtoTextUI("It appears to be a dagger. You pick it up.")
                # Add the dagger object to the players inventory list
                self.player.addItem(self.dagger)
                # See if the player would like to equip the weapon
                self.textUI.printtoTextUI("You should try to equip the dagger")
            # Set the rooms completed attribute to True
            self.currentRoom.completed = True
            # Continue story
            time.sleep(2)
            self.textUI.printtoTextUI("\nThe room now appears to be empty, you should move on")
        # Rove to next room
        elif self.currentRoom == self.corridor:
            time.sleep(2)
            # Inform player they should attack the creature
            self.textUI.printtoTextUI(f"A creature comes crawling out of the shadows, menacingly moving towards you")
            self.textUI.printtoTextUI("It's a Goblin, stand your ground and attack it, before it attacks you")
        # Move to next room
        elif self.currentRoom == self.hallroom:
            time.sleep(2)
            if self.currentRoom.completed != True:
                self.textUI.printtoTextUI("As you walk towards the end of the table you spot some bread on the table")
                self.textUI.printtoTextUI("You pocket it as you pass")
                self.textUI.printtoTextUI("You should eat it and replenish your health")
                # Add bread object to the players inventory
                self.player.addItem(self.hallroom_bread)
                
            # Set room.completed to True
            self.currentRoom.completed = True
        # Descend to next floor
        # Or return from baths/bedroom
        elif self.currentRoom == self.lounge:
            # Set room.completed to True
            self.currentRoom.completed = True
            time.sleep(2)
            # Suggest to the player that they trade
            self.textUI.printtoTextUI("\nYou should probably go and talk to the trader")
        # Move to next room
        elif self.currentRoom == self.baths:
            time.sleep(2)
            # Inform player there is a creature to attack
            self.textUI.printtoTextUI("A group of Bandits emerge from the water")
            self.textUI.printtoTextUI("A lone Bandit decides to confront you himself, you should make an example of him to scare the others off")
        # Move to next room
        elif self.currentRoom == self.bedroom:
            time.sleep(2)
            # Inform player there is a creature to attack
            self.textUI.printtoTextUI("A Goblin jumps out of nowhere and attacks")
        # Move to next room
        elif self.currentRoom == self.study:
            time.sleep(2)
            # Inform player there is an enemy to attack
            self.textUI.printtoTextUI("\nA large figure rises from where it was sat")
            self.textUI.printtoTextUI("'How arrogant to think you could walk into my study and just simply leave with your life'")
            self.textUI.printtoTextUI("\nMake sure you have something better than a dagger equiped before you confront this foe")
    # Move to the last room
        elif self.currentRoom == self.throneroom:
            time.sleep(2)
            # Inform player there is an enemy to defeat
            self.textUI.printtoTextUI("\n'So someone has finally come to dispose of me'")
            self.textUI.printtoTextUI("How insolent you are")
            self.textUI.printtoTextUI("\nCome, let me show you my power")
            

    def doAttack(self):
        """
            Performs attack functions for player and enemy
            :return: 1 if enemy is killed, 0 if player dies
        """
        # Instantiate variables to keep track of whether player/enemy is alive or dead
        player_dead = False
        enemy_dead = False
        # Use while loop to continuously check whether
        while player_dead == False:
            time.sleep(2)
            # Call player method of attack on target
            self.player.attack(self.currentRoom.enemy)
            # If enemy hp drops below 0
            if self.currentRoom.enemy.hp <= 0:
                self.textUI.printtoTextUI("You have killed the enemy")
                # Set enemy_dead to True and break from loop
                enemy_dead = True
                # Increase player gold by the amount of the enemies gold if it has any
                if self.currentRoom.enemy.gold != None:
                    self.player.gold += self.currentRoom.enemy.gold
                    time.sleep(2)
                    # Inform the player of the results of the looting
                    self.textUI.printtoTextUI(f"\nLooting the enemy gains you {self.currentRoom.enemy.gold}")
                    self.textUI.printtoTextUI(f"You now have {self.player.gold} gold pieces")
                break            
            time.sleep(2)
            # Call the rooms enemy attack method on player
            self.currentRoom.enemy.attackPlayer(self.player)
            # If player hp drops below 0 
            if self.player.hp <= 0:
                self.textUI.printtoTextUI("You have been slain")
                # Set player_dead to True, will end while loop
                player_dead = True
                
        
        if enemy_dead == True:
            # If enemy is killed, change it's alive attribute to false and return 1
            self.currentRoom.enemy.alive = False
            return 1
        # If player is killed return 0
        elif player_dead == True:
            return 0

    def doTrade(self):
        """
            Performs trader class trade method between player and trader
            :return: nothing
        
        """
        # Invoke a trader method to welcome player
        self.lounge_trader.welcomeSpeech()
        # Use if statment to check if a welcome gift has been given
        if self.lounge_trader.welcome == False:
            # If not, give gift
            self.lounge_trader.welcomeGift(self.player)
            # set welcome to True so it won't happen again
            self.lounge_trader.welcome = True
        # Start trading sequence
        self.lounge_trader.trade(self.player)
        # Exit speech
        self.lounge_trader.exitSpeech()

    def doEat(self):
        """
            Check that there are any of the games food items in the players inventory
            If not let the player now, ask for next command, else call player class method playerEat()
            return: Nothing
        """
        
        # Instantiate list with food names
        food_selection = ["BREAD", "MEAT", "POTATOES"]
        # Instantiate counter variable to keep track of the number of food objects in player inventory
        food_counter = 0
        # Iterate through player inventory
        for item in self.player.inventory:
            # Iterate though food selection
            for food in food_selection:
                # If the name of the item in player inventory matches that of the element in food selection
                if item.name.upper() == food:
                    # Increment counter
                    food_counter += 1
        # If the counter is 0, there are no food items in player inventory
        if food_counter == 0:
            self.textUI.printtoTextUI("\nYou have no food to eat sir")
        # If counter != 0
        else:
            # Call player method to eat 
            self.player.playerEat()
    
    def doEquip(self):
        """
            Check if player has weapons
            If so, perform player class method equipWeapon()
            return: nothing
        """
        # Instantiate list of weapon names
        weapon_selection = ["DAGGER", "SWORD", "AXE", "GREATSWORD", "BATTLEAXE"]
        food_bag = ["BREAD", "POTATOES", "MEAT"]
        # Instantiate counter variables
        weapon_counter = 0
        choice_counter = 0
        # Iterate through both player inventory and weapon selection to compare
        for i in self.player.inventory:
            for j in weapon_selection:
                if i.name.upper() == j:
                    # Print off any in both
                    self.textUI.printtoTextUI(i.name)
                    # Increase counter for every weapon in both
                    weapon_counter += 1
        # If counter = 0, then there are weapons in inventory
        if weapon_counter == 0:
            # Inform player there are no weapons in inventory
            self.textUI.printtoTextUI("\nThere are no weapons in your inventory to equip")
        # If counter is != 0
        else:
            # Use try/except clause to except player input nothing or just whitespace
            try:
                # Get weapon choice from player
                self.textUI.printtoTextUI("\nWhich weapon would you like to equip? ")
                # Get choice of weapon to equip
                weapon_choice = input().upper().replace(" ", "")
                # If the player does not have a weapon equiped,
                # Or the current equiped weapon is not the same as the player's choice
                if weapon_choice in food_bag:
                    self.textUI.printtoTextUI("\nYou can not equip food as a weapon")
                elif self.player.current_weapon == None or self.player.current_weapon.name.upper() != weapon_choice:
                    # Iterate through player inventory
                    for k in self.player.inventory:
                        # If the players weapon choice = a weapon.name in the inventory
                        if k.name.upper() == weapon_choice:
                            # Call player method to equip
                            self.player.equipWeapon(k)
                            # Increase counter
                            choice_counter += 1
                    # If the players choice does not match a weapon in their inventory, 
                    if choice_counter == 0:
                        self.textUI.printtoTextUI("\nSorry I didn't understand (your weapon choice should be one word)")
                # If the current equiped weapon is the same as the player's choice
                elif self.player.current_weapon.name.upper() == weapon_choice:
                    # Inform player of the fact
                    self.textUI.printtoTextUI("\nYou already have that weapon equiped")
            # Except index errors
            except IndexError as e:
                # Inform player of error
                self.textUI.printtoTextUI(f"\n{e}")
                self.textUI.printtoTextUI("You can't just enter whitespace")
            # Except attribute errors 
            except AttributeError as a:
                # Inform player of error
                self.textUI.printtoTextUI(f"\n{a}")
                self.textUI.printtoTextUI("You did not enter a choice")
    
    def doRemove(self):
        # If player inventory is empty
            if not self.player.inventory:
                # Inform player 
                self.textUI.printtoTextUI("\nThere are no items to remove")
            # If not empty
            else:
                # Enumerate through inventory and print
                for x, choice in enumerate(self.player.inventory):
                    self.textUI.printtoTextUI(f"{x}: {choice.name}")
                # Use try/except statement to catch exception
                try:
                    # Ask player to pick item number to remove
                    selection = int(input("Which item number would you like to remove? [ 9 to quit ]\n"))
                    # If input is 9
                    if selection == 9:
                        return False
                    else:
                        self.player.removeItem(self.player.inventory[selection])
                # If player chooses number out of index, except and inform player
                except IndexError as e:
                    self.textUI.printtoTextUI(f"\n{e}")
                    self.textUI.printtoTextUI("You need to input a number which corresponds to an item, or 9 to quit")
                # If a player tries to input a string, except and inform the player
                except ValueError as a:
                    self.textUI.printtoTextUI(f"\n{a}")
                    self.textUI.printtoTextUI("You need to input an integer number")
                



def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()