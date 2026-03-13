"""Player controller — pure Python logic (Ursina rendering wired in main.py)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from src.player.health import take_damage as _take_damage, heal as _heal, is_alive as _is_alive
from src.player.inventory import Inventory, ItemType
from src.world.block import BlockType

if TYPE_CHECKING:
    from src.world.world import World

Vec3 = Tuple[float, float, float]

REACH_DISTANCE = 5.0
MOVE_SPEED = 5.0
JUMP_VELOCITY = 8.0
DEFAULT_MAX_HEALTH = 20.0


class Player:
    """Pure-logic player state. Ursina entity wrappers are added in main.py."""

    def __init__(
        self,
        position: Vec3 = (0.0, 70.0, 0.0),
        max_health: float = DEFAULT_MAX_HEALTH,
    ) -> None:
        self.position: Vec3 = position
        self.rotation: Vec3 = (0.0, 0.0, 0.0)
        self.max_health: float = max_health
        self.health: float = max_health
        self.inventory: Inventory = Inventory()
        self.selected_slot: int = 0
        self.reach: float = REACH_DISTANCE
        self._spawn_position: Vec3 = position

    # ------------------------------------------------------------------
    # Movement (pure logic helpers — Ursina handles actual physics)
    # ------------------------------------------------------------------

    def move(self, direction: Vec3, dt: float) -> None:
        """Translate position in direction at MOVE_SPEED (used for tests / non-Ursina)."""
        dx, dy, dz = direction
        px, py, pz = self.position
        self.position = (
            px + dx * MOVE_SPEED * dt,
            py + dy * MOVE_SPEED * dt,
            pz + dz * MOVE_SPEED * dt,
        )

    def jump(self) -> None:
        """Signal a jump (Ursina physics integration done in main.py)."""
        pass

    # ------------------------------------------------------------------
    # Block interaction
    # ------------------------------------------------------------------

    def break_targeted_block(self, world: "World") -> Optional[ItemType]:
        """Break the block the player is looking at and add drop to inventory."""
        bx, by, bz = (int(round(v)) for v in self.position)
        # Simple approximation: break the block directly in front
        bx_target = bx
        by_target = by - 1  # below feet for now; Ursina raycasting replaces this
        bz_target = bz
        drop = world.break_block(bx_target, by_target, bz_target)
        if drop is not None:
            self.inventory.add_item(drop)
        return drop

    def place_block(self, world: "World") -> bool:
        """Place the selected block from inventory adjacent to the targeted block."""
        selected = self.inventory.get_selected_item()
        if selected is None:
            return False
        # Try to resolve ItemType → BlockType by name match
        try:
            block_type = BlockType[selected.item_type.name]
        except KeyError:
            return False
        bx, by, bz = (int(round(v)) for v in self.position)
        placed = world.place_block(bx, by - 2, bz, block_type)
        if placed:
            self.inventory.remove_item(selected.item_type)
        return placed

    # ------------------------------------------------------------------
    # Health
    # ------------------------------------------------------------------

    def take_damage(self, amount: float) -> None:
        self.health = _take_damage(self.health, amount, self.max_health)

    def heal(self, amount: float) -> None:
        self.health = _heal(self.health, amount, self.max_health)

    def is_alive(self) -> bool:
        return _is_alive(self.health)

    def respawn(self, spawn_position: Optional[Vec3] = None) -> None:
        self.health = self.max_health
        self.position = spawn_position if spawn_position is not None else self._spawn_position
