from __future__ import annotations

import math
from enum import Enum, auto
from typing import List, Optional, Tuple

from src.player.inventory import ItemType


class EnemyType(Enum):
    ZOMBIE = auto()
    SKELETON = auto()


class EnemyState(Enum):
    IDLE = auto()
    ALERT = auto()
    CHASE = auto()
    ATTACK = auto()
    DEAD = auto()


Vec3 = Tuple[float, float, float]


def _distance(a: Vec3, b: Vec3) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


# Loot tables per enemy type
LOOT_TABLES: dict[EnemyType, List[Tuple[ItemType, int]]] = {
    EnemyType.ZOMBIE:   [(ItemType.WOOD, 1)],
    EnemyType.SKELETON: [(ItemType.STONE, 1)],
}

ENEMY_STATS: dict[EnemyType, dict] = {
    EnemyType.ZOMBIE: {
        "max_health": 20.0,
        "damage": 2.0,
        "detection_range": 16.0,
        "attack_range": 2.0,
        "attack_cooldown": 1.5,
    },
    EnemyType.SKELETON: {
        "max_health": 16.0,
        "damage": 3.0,
        "detection_range": 20.0,
        "attack_range": 12.0,
        "attack_cooldown": 2.0,
    },
}


class Enemy:
    """Hostile NPC with a state-machine AI."""

    def __init__(
        self,
        position: Vec3,
        enemy_type: EnemyType = EnemyType.ZOMBIE,
    ) -> None:
        stats = ENEMY_STATS[enemy_type]
        self.position: Vec3 = position
        self.enemy_type: EnemyType = enemy_type
        self.max_health: float = stats["max_health"]
        self.health: float = self.max_health
        self.damage: float = stats["damage"]
        self.detection_range: float = stats["detection_range"]
        self.attack_range: float = stats["attack_range"]
        self.attack_cooldown: float = stats["attack_cooldown"]
        self._cooldown_timer: float = 0.0
        self.state: EnemyState = EnemyState.IDLE

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(self, player_position: Vec3, dt: float, is_night: bool) -> None:
        """Advance enemy AI state machine."""
        if self.state == EnemyState.DEAD:
            return

        dist = _distance(self.position, player_position)
        self._cooldown_timer = max(0.0, self._cooldown_timer - dt)

        if self.state == EnemyState.IDLE:
            if is_night and dist <= self.detection_range:
                self.state = EnemyState.ALERT

        elif self.state == EnemyState.ALERT:
            if not is_night or dist > self.detection_range:
                self.state = EnemyState.IDLE
            else:
                self.state = EnemyState.CHASE

        elif self.state == EnemyState.CHASE:
            if not is_night or dist > self.detection_range:
                self.state = EnemyState.IDLE
            elif dist <= self.attack_range:
                self.state = EnemyState.ATTACK
            else:
                self._move_towards(player_position, dt)

        elif self.state == EnemyState.ATTACK:
            if dist > self.attack_range:
                self.state = EnemyState.CHASE
            # Attack is resolved by the caller checking get_attack_damage()

    def take_damage(self, amount: float) -> Optional[List[Tuple[ItemType, int]]]:
        """Apply damage; returns loot list on death, None otherwise."""
        self.health = max(0.0, self.health - amount)
        if self.health <= 0:
            self.state = EnemyState.DEAD
            return list(LOOT_TABLES.get(self.enemy_type, []))
        return None

    def is_alive(self) -> bool:
        return self.state != EnemyState.DEAD and self.health > 0

    def get_attack_damage(self) -> float:
        return self.damage

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _move_towards(self, target: Vec3, dt: float, speed: float = 3.0) -> None:
        dist = _distance(self.position, target)
        if dist < 0.01:
            return
        dx = (target[0] - self.position[0]) / dist * speed * dt
        dz = (target[2] - self.position[2]) / dist * speed * dt
        self.position = (
            self.position[0] + dx,
            self.position[1],
            self.position[2] + dz,
        )
