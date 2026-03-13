"""Unit tests for SaveManager (User Story 5)."""
import os
import json
import pickle
import pytest
import tempfile

from src.world.world import World
from src.player.player import Player
from src.player.inventory import ItemType
from src.persistence.save_manager import SaveManager, WorldSave, SAVE_FORMAT_VERSION


@pytest.fixture
def tmp_saves(tmp_path):
    return str(tmp_path)


@pytest.fixture
def world():
    return World(seed=99)


@pytest.fixture
def player():
    p = Player()
    p.inventory.add_item(ItemType.WOOD, 10)
    return p


class TestSaveManager:
    def test_save_creates_files(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        result = sm.save(world, player, "test_save")
        assert result is True
        save_dir = os.path.join(tmp_saves, "test_save")
        assert os.path.exists(os.path.join(save_dir, "metadata.json"))
        assert os.path.exists(os.path.join(save_dir, "world.pkl"))

    def test_load_returns_world_save(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "test_save")
        ws = sm.load("test_save")
        assert ws is not None
        assert isinstance(ws, WorldSave)

    def test_load_nonexistent_returns_none(self, tmp_saves):
        sm = SaveManager(saves_dir=tmp_saves)
        assert sm.load("no_such_save") is None

    def test_list_saves_returns_names(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "alpha")
        sm.save(world, player, "beta")
        saves = sm.list_saves()
        assert "alpha" in saves
        assert "beta" in saves

    def test_delete_save_removes_directory(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "to_delete")
        assert sm.delete_save("to_delete") is True
        assert "to_delete" not in sm.list_saves()

    def test_delete_nonexistent_returns_false(self, tmp_saves):
        sm = SaveManager(saves_dir=tmp_saves)
        assert sm.delete_save("ghost") is False

    def test_round_trip_preserves_seed(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "rt")
        ws = sm.load("rt")
        assert ws.seed == world.seed

    def test_round_trip_preserves_player_health(self, tmp_saves, world, player):
        player.take_damage(5.0)
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "rt")
        ws = sm.load("rt")
        assert ws.player_health == player.health

    def test_round_trip_preserves_inventory(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "rt")
        ws = sm.load("rt")
        # Inventory items should be present in the save data
        item_types = [entry["item_type"] for entry in ws.player_inventory]
        assert "WOOD" in item_types

    def test_metadata_version_correct(self, tmp_saves, world, player):
        sm = SaveManager(saves_dir=tmp_saves)
        sm.save(world, player, "ver_test")
        ws = sm.load("ver_test")
        assert ws.version == SAVE_FORMAT_VERSION
