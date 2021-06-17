import unittest
from characters import Player, Trader, Enemy
import item
import Room

class TestCharacters(unittest.TestCase):

    def setUp(self):
        self.p1 = Player()
        self.dagger = item.Dagger()
        self.bread = item.Bread()
        self.t1 = Trader()
        self.e1 = Enemy(name="Goblin", hp=20, damage=10, alive=True, gold=30)

    def test_1(self):
        # Empty inventory returns false
        self.assertFalse(self.p1.printInventory())
        # add dagger to inventory 
        self.p1.addItem(self.dagger)
        # inventory should now have a dagger within, should rteturn true
        self.assertTrue(self.p1.printInventory())
        # inventory length should be 1
        self.assertEqual(len(self.p1.inventory),1)
        # remove dagger from inventory
        self.p1.removeItem(self.dagger)
        # printInventory should return false again as inventory empty
        self.assertFalse(self.p1.printInventory())
        # p1 hp should be 100
        self.assertEqual(self.p1.hp, 100)
        # e1 hp should be 20
        self.assertTrue(self.e1.hp, 20)
        # p1 should cause 5 damage to e1
        self.p1.attack(self.e1)
        # e1 hp should be 15 after the attack
        self.assertEqual(self.e1.hp, 15)
        # e1 should have 10 damage and 30 gold
        self.assertEqual(self.e1.damage, 10)
        self.assertEqual(self.e1.gold, 30)
        # e1 attack should cause damage to p1
        self.e1.attackPlayer(self.p1)
        # p1 should not have 100 hp
        self.assertNotEqual(self.p1.hp, 100)

    def test_2(self):
        # should fail as trade method catches Index errors and Value errors
        self.assertRaises(IndexError,self.t1.trade(self.p1))
        self.assertRaises(ValueError,self.t1.trade(self.p1))
        

def main():
    testing = TestCharacters()
    testing.setUp()
    testing.test_1()
    #testing.test_2()

if __name__ == "__main__":
    main()