import random
from Armor import Armor, armors


class Spell():

    def __init__(self, player, enemy, level):
        self.player = player
        self.enemy = enemy
        self.level = level


    def CastSpell(self, spell_name, armor=None):
        if spell_name not in Spells:
            print(f"{spell_name} is not a valid spell.")
            return

        spell = Spells[spell_name]
        element = spell[-1]
        spell_level = int(spell[1])

        damage = random.randint(1, self.level) * spell_level

        if armor is not None and armor.resistance:
            multiplier = armor.resistance.get(element, 1.0)
            damage = int(damage * multiplier)
            if multiplier < 1.0:
                print(f"{element} resisted! Damage reduced to {damage}!")
            elif multiplier > 1.0:
                print(f"{element} weakness! Damage increased to {damage}!")

        self.enemy.health -= damage
        print(f"{spell_name} deals {damage} {element} damage!")



    def PoisonSpell(self, spell_name, armor=None):
            if Spells[spell_name][-1] != "Poison":
                print(f"{spell_name} is not a Poison spell.")
                return
            self.Cast(spell_name, armor)
            print(f"{self.enemy} is poisoned!")


    def FireSpell(self, spell_name, armor=None):
        if Spells[spell_name][-1] != "Fire":
            print(f"{spell_name} is not a Fire spell.")
            return
        self.Cast(spell_name, armor)
        print(f"{self.enemy} is burning!")


    def IceSpell(self, spell_name, armor=None):
        if Spells[spell_name][-1] != "Ice":
            print(f"{spell_name} is not an Ice spell.")
            return
        self.Cast(spell_name, armor)


        freeze_chance = random.randint(1, 10)
        if freeze_chance <= 3:
            self.enemy.frozen = True
            print(f"{self.enemy} is frozen and will skip their next turn!")


    def LightningSpell(self, spell_name, armor=None):
        if Spells[spell_name][-1] != "Lighting":
            print(f"{spell_name} is not a Lighting spell.")
            return
        self.Cast(spell_name, armor)


Spells = {
        "Ember": ["1", "1", "Elemental", "Fire"],
        "Firebolt": ["2", "1", "Elemental", "Fire"],
        "Flamethrower": ["3", "1", "Elemental", "Fire"],
        "Blazing Inferno": ["4", "1", "Elemental", "Fire"],

        "Sting": ["5", "1", "Elemental", "Poison"],
        "Venomous bite ": ["6", "1", "Elemental", "Poison"],
        "Viper's Fangs": ["7", "1", "Elemental", "Poison"],
        "Toxic Destruction": ["8", "1", "Elemental", "Poison"],

        "Breeze": ["9", "1", "Elemental", "Ice"],
        "Ice bolt": ["10", "1", "Elemental", "Ice"],
        "Frozen Scythe": ["11", "1", "Elemental", "Ice"],
        "Total Tundra": ["12", "1", "Elemental", "Ice"],

        "Spark": ["13", "1", "Elemental", "Lighting"],
        "Thunder Strike": ["14", "2", "Elemental", "Lighting"],
        "Chain Lightning": ["15", "3", "Elemental", "Lighting"],
        "Storm Devastation": ["16", "4", "Elemental", "Lighting"],
    }

