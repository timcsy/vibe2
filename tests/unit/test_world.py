"""Unit tests for Chunk and World classes (User Story 1)."""
import pytest
from src.world.block import BlockType
from src.world.chunk import Chunk
from src.world.world import World


class TestChunk:
    def test_chunk_default_block_is_air(self):
        chunk = Chunk(position=(0, 0, 0))
        assert chunk.get_block(0, 0, 0) == BlockType.AIR

    def test_chunk_set_and_get_block(self):
        chunk = Chunk(position=(0, 0, 0))
        chunk.set_block(1, 2, 3, BlockType.STONE)
        assert chunk.get_block(1, 2, 3) == BlockType.STONE

    def test_chunk_sparse_storage_air_not_stored(self):
        chunk = Chunk(position=(0, 0, 0))
        chunk.set_block(0, 0, 0, BlockType.GRASS)
        assert (0, 0, 0) in chunk.blocks
        # Setting back to AIR removes from dict
        chunk.set_block(0, 0, 0, BlockType.AIR)
        assert (0, 0, 0) not in chunk.blocks

    def test_chunk_dirty_flag_set_on_block_change(self):
        chunk = Chunk(position=(0, 0, 0))
        chunk.is_dirty = False
        chunk.set_block(3, 3, 3, BlockType.DIRT)
        assert chunk.is_dirty is True

    def test_chunk_initial_state(self):
        chunk = Chunk(position=(1, 2, 3))
        assert chunk.position == (1, 2, 3)
        assert chunk.blocks == {}
        assert chunk.is_dirty is True
        assert chunk.is_loaded is False

    def test_chunk_set_multiple_blocks(self):
        chunk = Chunk(position=(0, 0, 0))
        chunk.set_block(0, 0, 0, BlockType.GRASS)
        chunk.set_block(1, 0, 0, BlockType.DIRT)
        chunk.set_block(2, 0, 0, BlockType.STONE)
        assert chunk.get_block(0, 0, 0) == BlockType.GRASS
        assert chunk.get_block(1, 0, 0) == BlockType.DIRT
        assert chunk.get_block(2, 0, 0) == BlockType.STONE


class TestWorld:
    def test_world_seed_determinism(self):
        world1 = World(seed=42)
        world2 = World(seed=42)
        # Same seed should produce same terrain at a given position
        assert world1.get_block(0, 0, 0) == world2.get_block(0, 0, 0)
        assert world1.get_block(5, 10, 5) == world2.get_block(5, 10, 5)

    def test_world_different_seeds_differ(self):
        world1 = World(seed=1)
        world2 = World(seed=9999)
        # Different seeds very likely produce different terrain
        blocks1 = [world1.get_block(x, 64, 0) for x in range(10)]
        blocks2 = [world2.get_block(x, 64, 0) for x in range(10)]
        assert blocks1 != blocks2

    def test_world_get_block_returns_block_type(self):
        world = World(seed=42)
        block = world.get_block(0, 0, 0)
        assert isinstance(block, BlockType)

    def test_world_set_block(self):
        world = World(seed=42)
        world.set_block(0, 0, 0, BlockType.STONE)
        assert world.get_block(0, 0, 0) == BlockType.STONE

    def test_world_break_block_returns_item(self):
        world = World(seed=42)
        world.set_block(0, 0, 0, BlockType.STONE)
        result = world.break_block(0, 0, 0)
        # Should return None or an ItemType name/string after breaking
        # After break the block should be AIR
        assert world.get_block(0, 0, 0) == BlockType.AIR

    def test_world_break_air_returns_none(self):
        world = World(seed=42)
        world.set_block(0, 0, 0, BlockType.AIR)
        result = world.break_block(0, 0, 0)
        assert result is None

    def test_world_place_block_returns_true_on_air(self):
        world = World(seed=42)
        world.set_block(0, 0, 0, BlockType.AIR)
        result = world.place_block(0, 0, 0, BlockType.STONE)
        assert result is True
        assert world.get_block(0, 0, 0) == BlockType.STONE

    def test_world_place_block_returns_false_on_occupied(self):
        world = World(seed=42)
        world.set_block(0, 0, 0, BlockType.STONE)
        result = world.place_block(0, 0, 0, BlockType.DIRT)
        assert result is False
        assert world.get_block(0, 0, 0) == BlockType.STONE

    def test_world_get_chunk(self):
        world = World(seed=42)
        chunk = world.get_chunk(0, 0, 0)
        assert chunk is not None
        assert chunk.position == (0, 0, 0)
