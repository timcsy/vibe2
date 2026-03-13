from __future__ import annotations

from typing import Dict, Tuple

from src.world.block import BlockType

CHUNK_SIZE = 16


class Chunk:
    """A 16×16×16 section of the voxel world stored as a sparse dict."""

    def __init__(self, position: Tuple[int, int, int]) -> None:
        self.position: Tuple[int, int, int] = position
        # Sparse storage — AIR blocks are omitted
        self.blocks: Dict[Tuple[int, int, int], BlockType] = {}
        self.is_dirty: bool = True
        self.is_loaded: bool = False

    def get_block(self, x: int, y: int, z: int) -> BlockType:
        """Return the block type at local position (x, y, z). Defaults to AIR."""
        return self.blocks.get((x, y, z), BlockType.AIR)

    def set_block(self, x: int, y: int, z: int, block_type: BlockType) -> None:
        """Set the block type at local position (x, y, z)."""
        if block_type == BlockType.AIR:
            self.blocks.pop((x, y, z), None)
        else:
            self.blocks[(x, y, z)] = block_type
        self.is_dirty = True
