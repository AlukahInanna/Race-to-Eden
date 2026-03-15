import random


class Weapon():

    def __init__(self):
        self.equipped_weapon = None


    def GetWeaponTemplate(self, player_class):
        if player_class not in ClassWeapons:
            print(f"{player_class} is not a valid class for weapon generation.")
            return

        return ClassWeapons[player_class]


    def GetRarityWeights(self, level):
        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 1

        if level <= 1:
            level = 1
 
        weights = {
            "Common": max(20, 65 - (level * 2)),
            "Uncommon": 22 + (level // 2),
            "Rare": 8 + level,
            "Epic": 3 + (level // 2),
            "Legendary": 1 + (level // 3),
        }

        return weights


    def RollRarity(self, level):
        weights = self.GetRarityWeights(level)
        rarity_names = list(weights.keys())
        rarity_weights = list(weights.values())
        return random.choices(rarity_names, weights=rarity_weights, k=1)[0]


    def BuildWeapon(self, player_class, level, rarity=None):
        template = self.GetWeaponTemplate(player_class)
        if not template:
            return
        try:
            level = int(level)
        except (TypeError, ValueError):
            level = 1
        if level <= 0:
            level = 1

        if rarity is None:
            rarity = self.RollRarity(level)

        if rarity not in RarityData:
            print(f"{rarity} is not a valid rarity.")
            return

        rarity_info = RarityData[rarity]
        multiplier = rarity_info["multiplier"]

        base_attack = template["base_attack"]
        scaled_attack = int(base_attack * multiplier)
        bonus_attack = max(1, int(level * 0.4 * multiplier))
        total_attack = scaled_attack + bonus_attack

        weapon = {
            "name": template["name"],
            "class": player_class,
            "weapon_type": template["weapon_type"],
            "rarity": rarity,
            "level_found": level,
            "attack_bonus": total_attack,
            "crit_chance": round(template["crit_chance"] + rarity_info["crit_bonus"], 3),
            "description": template["description"],
            "color": rarity_info["color"],
        }

        return weapon


    def FindWeaponForClass(self, level, player_class):
        weapon = self.BuildWeapon(player_class, level)
        if not weapon:
            return

        print(f"Found {weapon['rarity']} {weapon['name']} ({weapon['weapon_type']})!")
        return weapon


    def GetMapWeaponCount(self, level):
        # Placeholder until map spawning is integrated.
        return 0


    def NormalizeGrid(self, map_grid):
        # Placeholder until map spawning is integrated.
        return []


    def GetWalkableTiles(self, map_grid, blocked_chars=None, reserved_chars=None):
        # Placeholder until map spawning is integrated.
        return []


    def GenerateMapWeaponsFromGrid(self, level, map_grid, player_class=None):
        # Placeholder until map spawning is integrated.
        return []


    def PlaceWeaponsOnGrid(self, map_grid, weapon_drops, marker="w"):
        # Placeholder until map spawning is integrated.
        return []


    def GenerateLevelWeaponSpawns(self, level, level_grid, player_class=None):
        # Placeholder until map spawning is integrated.
        return {
            "level": level,
            "drops": [],
            "level_with_weapons": [],
        }


    def GenerateDefinedLevelWeaponSpawns(self, level_number, player_class=None):
        # Placeholder until map spawning is integrated.
        return {
            "level": level_number,
            "drops": [],
            "level_with_weapons": [],
        }


    def GenerateAllDefinedLevelWeaponSpawns(self, player_class=None):
        # Placeholder until map spawning is integrated.
        return []


    def GenerateMapWeapons(self, level, map_width, map_height, blocked_tiles=None, player_class=None):
        # Placeholder until map spawning is integrated.
        return []


    def EquipWeapon(self, player, weapon):
        if not player or not weapon:
            print("Player and weapon are required to equip.")
            return False

        if not hasattr(player, "attack"):
            print("Player does not support weapon equipping.")
            return False
        if not hasattr(player, "name"):
            print("Player is missing 'name' attribute.")
            return False
        if self.equipped_weapon is not None:
            player.attack -= self.equipped_weapon.get("attack_bonus", 0)

        self.equipped_weapon = weapon
        player.attack += weapon.get("attack_bonus", 0)

        print(f"{player.name} equipped {weapon['rarity']} {weapon['name']}!")
        return True


ClassWeapons = {
    "Knight": {
        "name": "Aegis Longsword",
        "weapon_type": "Sword",
        "base_attack": 10,
        "crit_chance": 0.08,
        "description": "A knight's balanced blade built for endurance and heavy strikes.",
    },
    "Rogue": {
        "name": "Shadowfang Twin Daggers",
        "weapon_type": "Dual Daggers",
        "base_attack": 8,
        "crit_chance": 0.16,
        "description": "A paired dagger set made for quick hits and critical bursts.",
    },
    "Mage": {
        "name": "Starweave Staff",
        "weapon_type": "Staff",
        "base_attack": 7,
        "crit_chance": 0.12,
        "description": "A channeling staff that amplifies arcane power with each tier.",
    },
}


RarityData = {
    "Common": {
        "multiplier": 1.00,
        "crit_bonus": 0.00,
        "color": "Gray",
    },
    "Uncommon": {
        "multiplier": 1.15,
        "crit_bonus": 0.01,
        "color": "Green",
    },
    "Rare": {
        "multiplier": 1.35,
        "crit_bonus": 0.02,
        "color": "Blue",
    },
    "Epic": {
        "multiplier": 1.60,
        "crit_bonus": 0.04,
        "color": "Purple",
    },
    "Legendary": {
        "multiplier": 1.95,
        "crit_bonus": 0.06,
        "color": "Gold",
    },
}
