from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class ItemType(Enum):
    WOOD = auto()
    STICK = auto()
    STONE = auto()
    COAL = auto()
    IRON_ORE = auto()
    IRON_INGOT = auto()
    WOOD_PLANKS = auto()
    WOOD_PICKAXE = auto()
    STONE_PICKAXE = auto()
    IRON_PICKAXE = auto()
    WOOD_SWORD = auto()
    STONE_SWORD = auto()
    IRON_SWORD = auto()
    TORCH = auto()
    CRAFTING_TABLE = auto()
    DIRT = auto()
    SAND = auto()


# Maximum stack sizes per item type
MAX_STACK_SIZES: dict[ItemType, int] = {
    ItemType.WOOD: 64,
    ItemType.STICK: 64,
    ItemType.STONE: 64,
    ItemType.COAL: 64,
    ItemType.IRON_ORE: 64,
    ItemType.IRON_INGOT: 64,
    ItemType.WOOD_PLANKS: 64,
    ItemType.WOOD_PICKAXE: 1,
    ItemType.STONE_PICKAXE: 1,
    ItemType.IRON_PICKAXE: 1,
    ItemType.WOOD_SWORD: 1,
    ItemType.STONE_SWORD: 1,
    ItemType.IRON_SWORD: 1,
    ItemType.TORCH: 64,
    ItemType.CRAFTING_TABLE: 64,
    ItemType.DIRT: 64,
    ItemType.SAND: 64,
}


@dataclass
class ItemStack:
    item_type: ItemType
    quantity: int
    max_stack: int = field(init=False)

    def __post_init__(self) -> None:
        self.max_stack = MAX_STACK_SIZES.get(self.item_type, 64)

    def __repr__(self) -> str:
        return f"ItemStack({self.item_type.name} x{self.quantity})"


class Inventory:
    def __init__(self, max_slots: int = 36, hotbar_size: int = 9) -> None:
        self.max_slots: int = max_slots
        self.hotbar_size: int = hotbar_size
        self.slots: List[Optional[ItemStack]] = [None] * max_slots
        self.selected_slot: int = 0

    def add_item(self, item_type: ItemType, quantity: int = 1) -> bool:
        """Add items to inventory. Returns True if all were added, False if inventory full."""
        remaining = quantity
        # First, try to stack with existing items
        for slot in self.slots:
            if slot is not None and slot.item_type == item_type:
                space = slot.max_stack - slot.quantity
                if space > 0:
                    add_amount = min(space, remaining)
                    slot.quantity += add_amount
                    remaining -= add_amount
                if remaining == 0:
                    return True
        # Then fill empty slots
        for i, slot in enumerate(self.slots):
            if slot is None and remaining > 0:
                max_stack = MAX_STACK_SIZES.get(item_type, 64)
                add_amount = min(max_stack, remaining)
                self.slots[i] = ItemStack(item_type=item_type, quantity=add_amount)
                remaining -= add_amount
            if remaining == 0:
                return True
        return remaining == 0

    def remove_item(self, item_type: ItemType, quantity: int = 1) -> bool:
        """Remove items from inventory. Returns True if removed, False if insufficient."""
        if not self.has_items(item_type, quantity):
            return False
        remaining = quantity
        for i, slot in enumerate(self.slots):
            if slot is not None and slot.item_type == item_type:
                take_amount = min(slot.quantity, remaining)
                slot.quantity -= take_amount
                remaining -= take_amount
                if slot.quantity == 0:
                    self.slots[i] = None
            if remaining == 0:
                return True
        return True

    def has_items(self, item_type: ItemType, quantity: int) -> bool:
        """Check if inventory contains at least quantity of item_type."""
        total = sum(
            slot.quantity for slot in self.slots
            if slot is not None and slot.item_type == item_type
        )
        return total >= quantity

    def get_hotbar(self) -> List[Optional[ItemStack]]:
        """Return the first hotbar_size slots."""
        return self.slots[:self.hotbar_size]

    def get_selected_item(self) -> Optional[ItemStack]:
        """Return the item in the currently selected hotbar slot."""
        return self.slots[self.selected_slot]

    def to_dict(self) -> List[dict]:
        """Serialize inventory for save files."""
        result = []
        for i, slot in enumerate(self.slots):
            if slot is not None:
                result.append({
                    "slot": i,
                    "item_type": slot.item_type.name,
                    "quantity": slot.quantity,
                })
        return result

    def from_dict(self, data: List[dict]) -> None:
        """Deserialize inventory from save file data."""
        self.slots = [None] * self.max_slots
        for entry in data:
            slot_index = entry["slot"]
            if 0 <= slot_index < self.max_slots:
                item_type = ItemType[entry["item_type"]]
                quantity = entry["quantity"]
                self.slots[slot_index] = ItemStack(item_type=item_type, quantity=quantity)
