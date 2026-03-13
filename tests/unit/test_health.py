"""Unit tests for Player health system (User Story 3)."""
import pytest
from src.player.player import Player
from src.player.health import take_damage, heal, is_alive


class TestHealthFunctions:
    def test_take_damage_reduces_health(self):
        assert take_damage(20.0, 5.0) == 15.0

    def test_take_damage_clamps_to_zero(self):
        assert take_damage(5.0, 100.0) == 0.0

    def test_heal_increases_health(self):
        assert heal(10.0, 5.0) == 15.0

    def test_heal_clamps_to_max(self):
        assert heal(19.0, 5.0, max_health=20.0) == 20.0

    def test_is_alive_true_when_positive(self):
        assert is_alive(1.0) is True

    def test_is_alive_false_when_zero(self):
        assert is_alive(0.0) is False

    def test_is_alive_false_when_negative(self):
        assert is_alive(-1.0) is False


class TestPlayerHealth:
    def test_player_starts_full_health(self):
        player = Player()
        assert player.health == player.max_health

    def test_take_damage_reduces_player_health(self):
        player = Player()
        player.take_damage(5.0)
        assert player.health == player.max_health - 5.0

    def test_take_damage_kills_player(self):
        player = Player()
        player.take_damage(100.0)
        assert not player.is_alive()
        assert player.health == 0.0

    def test_heal_restores_health(self):
        player = Player()
        player.take_damage(10.0)
        player.heal(5.0)
        assert player.health == player.max_health - 5.0

    def test_heal_does_not_exceed_max(self):
        player = Player()
        player.heal(100.0)
        assert player.health == player.max_health

    def test_is_alive_true_when_healthy(self):
        player = Player()
        assert player.is_alive() is True

    def test_is_alive_false_after_death(self):
        player = Player()
        player.take_damage(player.max_health)
        assert player.is_alive() is False

    def test_respawn_restores_full_health(self):
        player = Player()
        player.take_damage(100.0)
        player.respawn()
        assert player.health == player.max_health
        assert player.is_alive() is True

    def test_respawn_resets_position(self):
        spawn = (5.0, 70.0, 5.0)
        player = Player(position=spawn)
        player.take_damage(100.0)
        player.respawn()
        assert player.position == spawn
