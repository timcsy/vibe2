"""Contract test verifying metadata.json and world.pkl schema (User Story 5)."""
import json
import os
import pickle
import pytest

from src.world.world import World
from src.world.block import BlockType
from src.player.player import Player
from src.player.inventory import ItemType
from src.persistence.save_manager import SaveManager, SAVE_FORMAT_VERSION


@pytest.fixture
def saved_data(tmp_path):
    world = World(seed=42)
    world.set_block(0, 64, 0, BlockType.STONE)
    player = Player()
    player.inventory.add_item(ItemType.WOOD, 3)
    sm = SaveManager(saves_dir=str(tmp_path))
    sm.save(world, player, "contract_test")
    save_dir = os.path.join(str(tmp_path), "contract_test")
    with open(os.path.join(save_dir, "metadata.json")) as f:
        meta = json.load(f)
    with open(os.path.join(save_dir, "world.pkl"), "rb") as f:
        world_data = pickle.load(f)
    return meta, world_data


class TestSaveFormatContract:
    def test_metadata_has_version(self, saved_data):
        meta, _ = saved_data
        assert "version" in meta
        assert meta["version"] == SAVE_FORMAT_VERSION

    def test_metadata_has_save_name(self, saved_data):
        meta, _ = saved_data
        assert "save_name" in meta

    def test_metadata_has_save_timestamp(self, saved_data):
        meta, _ = saved_data
        assert "save_timestamp" in meta

    def test_metadata_has_seed(self, saved_data):
        meta, _ = saved_data
        assert "seed" in meta
        assert isinstance(meta["seed"], int)

    def test_metadata_has_day_time(self, saved_data):
        meta, _ = saved_data
        assert "day_time" in meta
        assert 0.0 <= meta["day_time"] <= 1.0

    def test_metadata_player_has_position(self, saved_data):
        meta, _ = saved_data
        assert "player" in meta
        assert "position" in meta["player"]
        assert len(meta["player"]["position"]) == 3

    def test_metadata_player_has_health(self, saved_data):
        meta, _ = saved_data
        assert "health" in meta["player"]
        assert isinstance(meta["player"]["health"], float)

    def test_metadata_player_has_inventory(self, saved_data):
        meta, _ = saved_data
        assert "inventory" in meta["player"]
        assert isinstance(meta["player"]["inventory"], list)

    def test_world_pkl_has_modified_chunks(self, saved_data):
        _, world_data = saved_data
        assert "modified_chunks" in world_data
        assert isinstance(world_data["modified_chunks"], dict)
