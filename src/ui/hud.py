"""HUD — pure-logic state for health bar and hotbar (Ursina rendering in main.py)."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.player.inventory import ItemStack, Inventory
    from src.player.player import Player

HOTBAR_SLOTS = 9


class HUD:
    """Tracks HUD state: health bar and hotbar selection."""

    def __init__(self) -> None:
        self.health: float = 20.0
        self.max_health: float = 20.0
        self.selected_slot: int = 0
        self._damage_flash: float = 0.0  # seconds remaining for flash

    def update(self, player: "Player", dt: float) -> None:
        self.health = player.health
        self.max_health = player.max_health
        self.selected_slot = player.selected_slot
        if self._damage_flash > 0:
            self._damage_flash = max(0.0, self._damage_flash - dt)

    def trigger_damage_flash(self, duration: float = 0.3) -> None:
        self._damage_flash = duration

    @property
    def is_flashing(self) -> bool:
        return self._damage_flash > 0

    def scroll_hotbar(self, delta: int) -> int:
        """Cycle selected_slot by delta steps (±1). Returns new slot index."""
        self.selected_slot = (self.selected_slot + delta) % HOTBAR_SLOTS
        return self.selected_slot

    def select_slot(self, index: int) -> None:
        """Directly select a hotbar slot (0-based)."""
        self.selected_slot = max(0, min(HOTBAR_SLOTS - 1, index))
