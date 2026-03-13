"""Health module helpers used by Player and Enemy."""
from __future__ import annotations


def take_damage(current: float, amount: float, max_health: float = 20.0) -> float:
    """Reduce health by amount, clamped to [0, max_health]."""
    return max(0.0, min(max_health, current - amount))


def heal(current: float, amount: float, max_health: float = 20.0) -> float:
    """Increase health by amount, clamped to [0, max_health]."""
    return max(0.0, min(max_health, current + amount))


def is_alive(current: float) -> bool:
    """Return True if health > 0."""
    return current > 0.0
