
import random


class Damage():

    def __init__(self, player, damage, enemy, level):
        self.player = player
        self.damage = damage
        self.enemy = enemy
        self.level = level

    def AttackDamage(self):
        damage = random.randint(1, self.level)
        self.enemy.health -= damage
        print(f"Dealt {damage} damage to {self.player.name}")


    def PoisonDamage(self):
        damage = random.randint(1, self.level)
        self.enemy.health -= damage
        print(f"Dealt {damage} poison damage!")


    def LightningDamage(self):
        damage = random.randint(1, self.level)
        self.enemy.health -= damage
        print(f"Dealt {damage} lightning damage!")


    def FireDamage(self):
        damage = random.randint(1, self.level)
        self.enemy.health -= damage
        print(f"Dealt {damage} burn damage!")


    def IceDamage(self):
        damage = random.randint(1, self.level)
        self.enemy.health -= damage
        print(f"Dealt {damage} ice damage!")


    def LifeLeech(self):
        lifeleech = random.randint(1, self.level)
        self.player.health += lifeleech
        self.enemy.health -= lifeleech


    def Kill(self, character):
        character.health = 0













