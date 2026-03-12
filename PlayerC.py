import random


class Player():

    def __init__(self, name, player_class="Knight", level=1):
        if player_class not in PlayerClasses:
            raise ValueError(f"{player_class} is not a valid class. Choose Mage, Rogue, or Knight.")

        base = PlayerClasses[player_class]

        self.name = name
        self.player_class = player_class
        self.level = level

        self.max_health = base["health"]
        self.max_mana = base["mana"]
        self.max_stamina = base["stamina"]

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

        self.attack = base["attack"]
        self.defense = base["defense"]

        self.exp = 0
        self.gold = 0

        self.alive = True
        self.in_combat = False

        self.poisoned = False
        self.frozen = False

        self.active_buffs = {
            "strength_buff": 0,
            "defense_buff": 0,
        }
        self.shield = 0


    def ShowStats(self):
        print(f"{self.name} | {self.player_class} | Level {self.level}")
        print(f"HP: {self.health}/{self.max_health}")
        print(f"MP: {self.mana}/{self.max_mana}")
        print(f"ST: {self.stamina}/{self.max_stamina}")
        print(f"ATK: {self.attack} | DEF: {self.defense}")
        print(f"Poisoned: {self.poisoned} | Frozen: {self.frozen} | Shield: {self.shield}")


    def StartCombat(self):
        self.in_combat = True


    def EndCombat(self):
        self.in_combat = False

    def AttackTarget(self, enemy):
        if not self.alive:
            print(f"{self.name} cannot attack while dead.")
            return 0

        if self.frozen:
            print(f"{self.name} is frozen and misses the turn.")
            self.frozen = False
            return 0

        min_damage = max(1, self.attack // 2)
        damage = random.randint(min_damage, self.attack + self.level)

        if self.active_buffs["strength_buff"] > 0:
            damage = int(damage * 1.3)

        enemy.health = max(0, enemy.health - damage)
        if enemy.health == 0 and hasattr(enemy, "Die") and getattr(enemy, "alive", True):
            enemy.Die()

        print(f"{self.name} dealt {damage} damage to {enemy.name}.")
        return damage


    def TakeDamage(self, damage):
        if not self.alive:
            return 0

        reduced = max(0, int(damage - self.defense))

        if self.active_buffs["defense_buff"] > 0:
            reduced = int(reduced * 0.7)

        if self.shield > 0:
            absorbed = min(self.shield, reduced)
            self.shield -= absorbed
            reduced -= absorbed
            print(f"Shield absorbed {absorbed} damage.")

        self.health -= reduced

        if self.health <= 0:
            self.health = 0
            self.Die()

        print(f"{self.name} took {reduced} damage. HP: {self.health}/{self.max_health}")
        return reduced


    def Heal(self, amount):
        if amount <= 0:
            return 0

        old = self.health
        self.health = min(self.max_health, self.health + amount)
        healed = self.health - old
        print(f"{self.name} healed {healed} HP.")
        return healed


    def UseMana(self, amount):
        if amount > self.mana:
            print("Not enough mana.")
            return False

        self.mana -= amount
        return True


    def UseStamina(self, amount):
        if amount > self.stamina:
            print("Not enough stamina.")
            return False

        self.stamina -= amount
        return True


    def RestorePercent(self, resource, percent):
        if percent <= 0:
            return 0

        if resource == "hp":
            amount = int(self.max_health * percent)
            return self.Heal(amount)

        if resource == "mp":
            amount = int(self.max_mana * percent)
            old = self.mana
            self.mana = min(self.max_mana, self.mana + amount)
            restored = self.mana - old
            print(f"{self.name} restored {restored} MP.")
            return restored

        if resource == "st":
            amount = int(self.max_stamina * percent)
            old = self.stamina
            self.stamina = min(self.max_stamina, self.stamina + amount)
            restored = self.stamina - old
            print(f"{self.name} restored {restored} ST.")
            return restored

        return 0


    def TickTurn(self):
        if self.active_buffs["strength_buff"] > 0:
            self.active_buffs["strength_buff"] -= 1

        if self.active_buffs["defense_buff"] > 0:
            self.active_buffs["defense_buff"] -= 1

        if self.poisoned and self.alive:
            poison_damage = max(1, int(self.max_health * 0.05))
            self.TakeDamage(poison_damage)


    def GainExp(self, amount):
        if amount <= 0:
            return

        self.exp += amount
        needed = self.level * 100

        while self.exp >= needed:
            self.exp -= needed
            self.LevelUp()
            needed = self.level * 100


    def LevelUp(self):
        self.level += 1
        self.max_health += 10
        self.max_mana += 8
        self.max_stamina += 8
        self.attack += 2
        self.defense += 1

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

        print(f"{self.name} leveled up to {self.level}!")


    def Die(self):
        self.alive = False
        print(f"{self.name} has fallen.")


    def Revive(self, hp_percent=0.40):
        if hp_percent <= 0:
            hp_percent = 0.40

        self.health = max(1, int(self.max_health * hp_percent))
        self.alive = True
        self.poisoned = False
        self.frozen = False
        print(f"{self.name} revived with {self.health} HP.")


PlayerClasses = {
    "Mage": {
        "health": 90,
        "mana": 130,
        "stamina": 80,
        "attack": 14,
        "defense": 4,
    },
    "Rogue": {
        "health": 105,
        "mana": 85,
        "stamina": 120,
        "attack": 13,
        "defense": 6,
    },
    "Knight": {
        "health": 140,
        "mana": 60,
        "stamina": 95,
        "attack": 11,
        "defense": 9,
    },
}
