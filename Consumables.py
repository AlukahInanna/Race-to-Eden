class Consumables():

    def __init__(self):
        self.inventory = {}


    def AddConsumable(self, consumable_name, amount=1):
        if consumable_name not in ConsumablesData:
            print(f"{consumable_name} is not a valid consumable.")
            return

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        data = ConsumablesData[consumable_name]
        max_stack = data[6]
        current = self.inventory.get(consumable_name, 0)
        added = min(amount, max_stack - current)

        if added <= 0:
            print(f"{consumable_name} stack is full ({max_stack}).")
            return

        self.inventory[consumable_name] = current + added
        print(f"Added {added}x {consumable_name}. Total: {self.inventory[consumable_name]}")


    def UseConsumable(self, consumable_name, in_combat=False, poisoned=False, shield_active=False, active_buffs=None, player=None):
        if consumable_name not in ConsumablesData:
            print(f"{consumable_name} is not a valid consumable.")
            return

        if self.inventory.get(consumable_name, 0) <= 0:
            print(f"No {consumable_name} in inventory.")
            return

        if player is not None:
            in_combat = getattr(player, "in_combat", in_combat)
            poisoned = getattr(player, "poisoned", poisoned)
            shield_active = getattr(player, "shield", 0) > 0
            active_buffs = getattr(player, "active_buffs", active_buffs)

        if active_buffs is None:
            active_buffs = {}

        data = ConsumablesData[consumable_name]
        effect = data[2]
        use_scope = data[5]

        if use_scope == "combat" and not in_combat:
            print(f"{consumable_name} can only be used in combat.")
            return

        if effect == "cure_poison" and not poisoned:
            print("Antidote failed: target is not poisoned.")
            return

        if effect == "shield" and shield_active:
            print("Shield Potion failed: shield is already active.")
            return

        if effect in ["strength_buff", "defense_buff"] and active_buffs.get(effect, 0) > 0:
            print(f"{consumable_name} failed: same buff is already active.")
            return

        if effect == "auto_revive":
            print("Revival Scroll triggers automatically and cannot be used manually.")
            return

        self.inventory[consumable_name] -= 1
        if self.inventory[consumable_name] <= 0:
            del self.inventory[consumable_name]

        payload = self.GetEffectData(consumable_name)
        print(f"Used {consumable_name}. Remaining: {self.inventory.get(consumable_name, 0)}")

        if player is not None:
            self.ApplyEffectToPlayer(player, payload)

        return payload


    def UseConsumableOnPlayer(self, player, consumable_name):
        return self.UseConsumable(consumable_name, player=player)


    def GetEffectData(self, consumable_name):
        if consumable_name not in ConsumablesData:
            return

        data = ConsumablesData[consumable_name]

        result = {
            "effect": data[2],
            "resource": data[3],
            "value": data[4],
            "duration": data[7],
        }

        if result["duration"] == 0:
            del result["duration"]

        return result


    def ApplyEffectToPlayer(self, player, effect_data):
        if player is None:
            print("No player target provided.")
            return

        if not effect_data:
            print("No consumable effect to apply.")
            return

        effect = effect_data.get("effect")

        if effect == "restore":
            if hasattr(player, "RestorePercent"):
                player.RestorePercent(effect_data.get("resource"), effect_data.get("value", 0))
            return

        if effect == "cure_poison":
            player.poisoned = False
            print(f"{player.name} is cured from poison.")
            return

        if effect in ["strength_buff", "defense_buff"]:
            player.active_buffs[effect] = effect_data.get("duration", 3)
            print(f"{effect} applied for {player.active_buffs[effect]} turns.")
            return

        if effect == "shield":
            if player.shield > 0:
                print("Shield is already active.")
                return
            player.shield = int(player.max_health * effect_data.get("value", 0.40))
            print(f"Shield applied: {player.shield}")
            return

        if effect == "auto_revive":
            if player.alive:
                return
            if hasattr(player, "Revive"):
                player.Revive(effect_data.get("value", 0.30))
            return


    def HealthPotion(self, consumable_name, in_combat=False, player=None):
        if "Health Potion" not in consumable_name:
            print(f"{consumable_name} is not a Health Potion.")
            return
        return self.UseConsumable(consumable_name, in_combat=in_combat, player=player)


    def ManaPotion(self, consumable_name, in_combat=False, player=None):
        if "Mana Potion" not in consumable_name:
            print(f"{consumable_name} is not a Mana Potion.")
            return
        return self.UseConsumable(consumable_name, in_combat=in_combat, player=player)


    def StaminaPotion(self, consumable_name, in_combat=False, player=None):
        if "Stamina Potion" not in consumable_name:
            print(f"{consumable_name} is not a Stamina Potion.")
            return
        return self.UseConsumable(consumable_name, in_combat=in_combat, player=player)


    def Antidote(self, in_combat=False, poisoned=False, player=None):
        return self.UseConsumable("Antidote", in_combat=in_combat, poisoned=poisoned, player=player)


    def StrengthPotion(self, in_combat=False, active_buffs=None, player=None):
        return self.UseConsumable("Strength Potion", in_combat=in_combat, active_buffs=active_buffs, player=player)


    def DefensePotion(self, in_combat=False, active_buffs=None, player=None):
        return self.UseConsumable("Defense Potion", in_combat=in_combat, active_buffs=active_buffs, player=player)


    def ShieldPotion(self, in_combat=False, shield_active=False, player=None):
        return self.UseConsumable("Shield Potion", in_combat=in_combat, shield_active=shield_active, player=player)


    def TryAutoRevive(self, player=None):
        scroll_name = "Revival Scroll"

        if self.inventory.get(scroll_name, 0) <= 0:
            return

        self.inventory[scroll_name] -= 1
        if self.inventory[scroll_name] <= 0:
            del self.inventory[scroll_name]

        print("Revival Scroll triggered automatically.")
        payload = self.GetEffectData(scroll_name)

        if player is not None:
            self.ApplyEffectToPlayer(player, payload)

        return payload


PotionSizes = {
    "Small": 0.25,
    "Medium": 0.50,
    "Large": 1.00,
}

PotionResources = {
    "Health": "hp",
    "Mana": "mp",
    "Stamina": "st",
}


def BuildRestorePotions(start_id=1):
    data = {}
    item_id = start_id

    for potion_name, resource in PotionResources.items():
        for size_name, value in PotionSizes.items():
            full_name = f"{potion_name} Potion ({size_name})"
            data[full_name] = [str(item_id), "Potion", "restore", resource, value, "both", 10, 0]
            item_id += 1

    return data, item_id


ConsumablesData, next_id = BuildRestorePotions(1)
ConsumablesData.update({
    "Antidote": [str(next_id), "Potion", "cure_poison", None, 0, "both", 5, 0],
    "Strength Potion": [str(next_id + 1), "Potion", "strength_buff", None, 0.30, "combat", 5, 3],
    "Defense Potion": [str(next_id + 2), "Potion", "defense_buff", None, 0.30, "combat", 5, 3],
    "Shield Potion": [str(next_id + 3), "Potion", "shield", None, 0.40, "combat", 3, 0],
    "Revival Scroll": [str(next_id + 4), "Scroll", "auto_revive", "hp", 0.30, "auto", 2, 0],
})
