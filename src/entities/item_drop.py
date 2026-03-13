"""ItemDrop entity — dropped item that can be picked up by the player."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING, Tuple

from src.player.inventory import ItemType

if TYPE_CHECKING:
    from src.player.player import Player

Vec3 = Tuple[float, float, float]

PICKUP_RADIUS = 2.0
DESPAWN_TIME = 300.0  # seconds before auto-despawn


class ItemDrop:
    """A dropped item sitting in the world. Pure logic; Ursina entity in main.py."""

    def __init__(self, position: Vec3, item_type: ItemType, quantity: int = 1) -> None:
        self.position: Vec3 = position
        self.item_type: ItemType = item_type
        self.quantity: int = quantity
        self._alive: bool = True
        self._age: float = 0.0

    def is_alive(self) -> bool:
        return self._alive

    def update(self, player: "Player", dt: float) -> bool:
        """Return True if the item was collected this frame."""
        if not self._alive:
            return False
        self._age += dt
        if self._age >= DESPAWN_TIME:
            self._alive = False
            return False
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(self.position, player.position)))
        if dist <= PICKUP_RADIUS:
            collected = player.inventory.add_item(self.item_type, self.quantity)
            if collected:
                self._alive = False
                return True
        return False
