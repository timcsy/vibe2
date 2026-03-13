"""Unit tests for Enemy state-machine (User Story 3)."""
import pytest
from src.entities.enemy import Enemy, EnemyType, EnemyState

PLAYER_FAR = (1000.0, 0.0, 1000.0)
PLAYER_NEAR = (5.0, 0.0, 0.0)       # within detection_range (16) but outside attack_range (2)
PLAYER_ADJACENT = (0.5, 0.0, 0.0)   # within attack_range (2)


class TestEnemyStateMachine:
    def _enemy(self) -> Enemy:
        return Enemy(position=(0.0, 0.0, 0.0), enemy_type=EnemyType.ZOMBIE)

    def test_enemy_starts_idle(self):
        enemy = self._enemy()
        assert enemy.state == EnemyState.IDLE

    def test_idle_to_alert_when_player_near_at_night(self):
        enemy = self._enemy()
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.ALERT

    def test_idle_stays_idle_when_player_far(self):
        enemy = self._enemy()
        enemy.update(PLAYER_FAR, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.IDLE

    def test_idle_stays_idle_during_day(self):
        enemy = self._enemy()
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=False)
        assert enemy.state == EnemyState.IDLE

    def test_alert_to_chase(self):
        enemy = self._enemy()
        enemy.state = EnemyState.ALERT
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.CHASE

    def test_chase_to_attack_when_adjacent(self):
        enemy = self._enemy()
        enemy.state = EnemyState.CHASE
        enemy.update(PLAYER_ADJACENT, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.ATTACK

    def test_attack_to_chase_when_player_moves_away(self):
        enemy = self._enemy()
        enemy.state = EnemyState.ATTACK
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.CHASE

    def test_chase_to_idle_during_day(self):
        enemy = self._enemy()
        enemy.state = EnemyState.CHASE
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=False)
        assert enemy.state == EnemyState.IDLE

    def test_take_damage_reduces_health(self):
        enemy = self._enemy()
        initial = enemy.health
        result = enemy.take_damage(5.0)
        assert enemy.health == initial - 5.0
        assert result is None  # not dead yet

    def test_take_damage_kills_enemy(self):
        enemy = self._enemy()
        loot = enemy.take_damage(enemy.max_health + 10)
        assert enemy.state == EnemyState.DEAD
        assert not enemy.is_alive()
        assert loot is not None
        assert len(loot) > 0

    def test_dead_enemy_does_not_update(self):
        enemy = self._enemy()
        enemy.state = EnemyState.DEAD
        enemy.update(PLAYER_NEAR, dt=0.1, is_night=True)
        assert enemy.state == EnemyState.DEAD

    def test_get_attack_damage_positive(self):
        enemy = self._enemy()
        assert enemy.get_attack_damage() > 0
