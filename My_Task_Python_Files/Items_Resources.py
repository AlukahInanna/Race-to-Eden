

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ItemType(Enum):
    HEALTH_POTION = "Health Potion"
    STAMINA_POTION = "Stamina Potion"
    MAGIC_POTION = "Magic Potion"
    SWORD = "Sword"
    AXE = "Axe"
    BOW = "Bow"
    SHIELD = "Shield"
    HELMET = "Helmet"
    ARMOR = "Armor"


# simple ASCII rendering in a tile map
ITEM_GLYPH: Dict[ItemType, str] = {
    ItemType.HEALTH_POTION: "h",
    ItemType.STAMINA_POTION: "s",
    ItemType.MAGIC_POTION: "m",
    ItemType.SWORD: "/",
    ItemType.AXE: "A",
    ItemType.BOW: ")",
    ItemType.SHIELD: "[",
    ItemType.HELMET: "^",
    ItemType.ARMOR: "=",
}


@dataclass
class Inventory:
    consumables: Dict[ItemType, int] = field(default_factory=dict)
    weapons: List[ItemType] = field(default_factory=list)
    shields: List[ItemType] = field(default_factory=list)
    gear: List[ItemType] = field(default_factory=list)  # helmet, armor, etc.
    equipped_weapon: Optional[ItemType] = None
    equipped_shield: Optional[ItemType] = None

    def pick_up(self, item: ItemType) -> None:

        if item in (ItemType.HEALTH_POTION, ItemType.STAMINA_POTION, ItemType.MAGIC_POTION):
            self.consumables[item] = self.consumables.get(item, 0) + 1
        elif item in (ItemType.SWORD, ItemType.AXE, ItemType.BOW):
            self.weapons.append(item)
        elif item == ItemType.SHIELD:
            self.shields.append(item)
        else:
            self.gear.append(item)

    def use_consumable(self, item: ItemType) -> str:
        if self.consumables.get(item, 0) <= 0:
            return f"No {item.value} in inventory."
        self.consumables[item] -= 1
        return f"Used {item.value}."

    def equip_weapon(self, item: ItemType) -> bool:
        if item not in self.weapons:
            return False
        self.equipped_weapon = item
        return True

    def equip_shield(self, item: ItemType) -> bool:
        if item not in self.shields:
            return False
        self.equipped_shield = item
        return True

    def __str__(self) -> str:
        lines: List[str] = []
        consumables_list = [f"{it.value} x{count}" for it, count in self.consumables.items() if count]
        if consumables_list:
            lines.append("Consumables:")
            lines.extend("  " + s for s in consumables_list)
        if self.weapons:
            lines.append("Weapons: " + ", ".join(i.value for i in self.weapons))
        if self.shields:
            lines.append("Shields: " + ", ".join(i.value for i in self.shields))
        if self.gear:
            lines.append("Gear: " + ", ".join(i.value for i in self.gear))
        if self.equipped_weapon:
            lines.append(f"Equipped weapon: {self.equipped_weapon.value}")
        if self.equipped_shield:
            lines.append(f"Equipped shield: {self.equipped_shield.value}")
        return "\n".join(lines) if lines else "(empty inventory)"



__all__ = [
    "ItemType", "ITEM_GLYPH", "Inventory",
]


if __name__ == "__main__":
    # basic demonstration of behaviour
    inv = Inventory()
    inv.pick_up(ItemType.HEALTH_POTION)
    inv.pick_up(ItemType.HEALTH_POTION)
    inv.pick_up(ItemType.SWORD)
    inv.pick_up(ItemType.SHIELD)
    print(inv)
    print(inv.use_consumable(ItemType.HEALTH_POTION))
    print(inv)
    inv.equip_weapon(ItemType.SWORD)
    inv.equip_shield(ItemType.SHIELD)
    print(inv)
