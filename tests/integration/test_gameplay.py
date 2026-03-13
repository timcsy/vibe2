"""Integration test covering full gameplay flow (world gen → move → break → craft → save → load)."""
import os
import pytest

from src.world.world import World
from src.world.block import BlockType
from src.player.player import Player
from src.player.inventory import ItemType
from src.crafting.recipe import build_default_registry
from src.crafting.crafting_ui import CraftingUI
from src.persistence.save_manager import SaveManager


class TestGameplayFlow:
    def test_world_generation_produces_terrain(self):
        world = World(seed=1337)
        # At some y level near sea level there should be solid blocks
        has_solid = any(
            world.get_block(x, 63, z) != BlockType.AIR
            for x in range(5) for z in range(5)
        )
        assert has_solid

    def test_player_can_move(self):
        player = Player(position=(0.0, 70.0, 0.0))
        initial = player.position
        player.move((1.0, 0.0, 0.0), dt=1.0)
        assert player.position[0] > initial[0]

    def test_break_block_adds_to_inventory(self):
        world = World(seed=42)
        player = Player()
        world.set_block(0, 63, 0, BlockType.STONE)
        drop = world.break_block(0, 63, 0)
        if drop is not None:
            player.inventory.add_item(drop)
            assert player.inventory.has_items(drop, 1)
        assert world.get_block(0, 63, 0) == BlockType.AIR

    def test_craft_wood_planks(self):
        registry = build_default_registry()
        ui = CraftingUI(registry)
        player = Player()
        player.inventory.add_item(ItemType.WOOD, 1)
        ui.open()
        ui.set_slot(0, 0, ItemType.WOOD)
        result = ui.craft(player.inventory)
        assert result == ItemType.WOOD_PLANKS
        assert player.inventory.has_items(ItemType.WOOD_PLANKS, 4)

    def test_save_and_load_preserves_state(self, tmp_path):
        world = World(seed=777)
        player = Player(position=(10.0, 65.0, 10.0))
        player.inventory.add_item(ItemType.WOOD, 5)
        player.take_damage(3.0)

        sm = SaveManager(saves_dir=str(tmp_path))
        assert sm.save(world, player, "gameplay_test") is True

        ws = sm.load("gameplay_test")
        assert ws is not None
        assert ws.seed == 777
        assert abs(ws.player_position[0] - 10.0) < 0.01
        assert abs(ws.player_health - player.health) < 0.01
        item_types = [e["item_type"] for e in ws.player_inventory]
        assert "WOOD" in item_types

    def test_day_night_cycle_advances(self):
        world = World(seed=42)
        initial_time = world.day_time
        world.update(dt=100.0)
        assert world.day_time != initial_time

    def test_enemy_detects_player_at_night(self):
        from src.entities.enemy import Enemy, EnemyType, EnemyState
        enemy = Enemy(position=(0.0, 0.0, 0.0))
        player_pos = (5.0, 0.0, 5.0)
        enemy.update(player_pos, dt=0.1, is_night=True)
        assert enemy.state != EnemyState.IDLE
