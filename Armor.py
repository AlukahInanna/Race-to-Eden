import pygame
import random




class Armor(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, level):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.resistance = {}
        self.level = level



    def Elemental(self, armor):
        self.armor = armor

        if "Elemental" in armors[armor]:
            element_type = armors[armor][-1]

            # Calculate resistance based on element type
            resistance_table = {
                "Fire": {"Fire": 0.5, "Ice": 1.5, "Poison": 1.0, "Lighting": 1.0},
                "Ice": {"Fire": 1.5, "Ice": 0.5, "Poison": 1.0, "Lighting": 1.0},
                "Poison": {"Fire": 1.0, "Ice": 1.0, "Poison": 0.5, "Lighting": 1.5},
                "Lighting": {"Fire": 1.0, "Ice": 1.0, "Poison": 1.5, "Lighting": 0.5},
            }

            self.resistance = resistance_table.get(element_type, {})
            print(f"{armor} equipped! Resistances: {self.resistance}")

        else:
            print(f"{armor} is not an Elemental armor.")
            self.resistance = {}



    def Buffed (self, armor, damage, enemy = None):

        self.armor = armor

        if "Buffed" not in armors[armor]:
            print(f"{armor} is not a Buffed armor.")
            return damage

        buff = armors[armor][3]

        match buff: #Dodge
            case 1:
                dodgechance = random.randint(1, 10)
                if dodgechance <=3:
                    damage = 0
                    print("Dodged Attack!")
            case 2: #Endurance
                damage = int(damage * 0.7)
                print(f"Endurance activated! Damage reduced to {damage}!")

            case 3: #Reflect
                reflectchance = random.randint(1, 10)
                if reflectchance <= 3 and enemy != None:
                    print(f"Attack reflected! Enemy Suffers {damage} damage! ")

        return damage


    def Special(self, armor,player, damage, enemy, Boss,):

        if "Special" not in armors[armor]:
            print(f"{armor} is not a Special armor.")
            return damage

        special = armors[armor][3]

        match special:

            case 1:
                chance = random.randint(1, 10)
                if chance <= 1 and enemy != Boss:
                    enemy.health = 0

            case 2:
                damage = int(damage * 0.7)
                if random.randint(1, 10) <=3:
                    damage = 0

            case 3:
                healing = random.randint(1, 10)
                if healing <=3:
                    player.health += healing * 10


        return damage




armors = {

        #Armor Name : [Armor ID, Armor Level, Armor Type]

        "Armor of Fire" : [ "1" , "1", "Elemental", "Fire"],
        "Armor of Poison" : [ "2" , "1","Elemental", "Poison"],
        "Armor of Ice" : [ "3" , "1","Elemental", "Ice" ],
        "Armor of Lighting" : [ "4" , "1","Elemental", "Lighting"],

        "Armor of Shadow" : [ "5" , "1","Buffed", 1],
        "Armor of Endurance" : [ "6" , "1","Buffed", 2],
        "Armor of Reflection": ["7", "1", "Buffed", 3],

        "Armor of Rayleigh": [ "8" , "1", "Special",1],
        "Armor of Kaldor": [ "9" , "1", "Special",2],
        "Armor of Eden" : [ "10" , "1", "Special", 3]
    }
