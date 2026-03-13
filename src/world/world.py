from __future__ import annotations

import math
from typing import Dict, Optional, Tuple

try:
    import noise  # type: ignore
    HAS_NOISE = True
except ImportError:  # pragma: no cover
    HAS_NOISE = False

from src.world.block import BlockType, get_block_properties
from src.world.chunk import Chunk, CHUNK_SIZE
from src.player.inventory import ItemType

WORLD_HEIGHT = 128
SEA_LEVEL = 64
TERRAIN_SCALE = 0.03


def _terrain_height(seed: int, x: int, z: int) -> int:
    """Return the surface Y coordinate for world (x, z) using Perlin noise."""
    if HAS_NOISE:
        val = noise.pnoise2(
            x * TERRAIN_SCALE + seed * 0.1,
            z * TERRAIN_SCALE + seed * 0.1,
            octaves=4,
            persistence=0.5,
            lacunarity=2.0,
        )
    else:
        # Fallback deterministic height without the noise library
        import hashlib
        h = int(hashlib.md5(f"{seed}{x}{z}".encode()).hexdigest(), 16)
        val = (h % 1000) / 1000.0 - 0.5

    height = int(SEA_LEVEL + val * 20)
    return max(1, min(WORLD_HEIGHT - 1, height))


class World:
    """Manages the voxel world, procedural generation, and day/night cycle."""

    def __init__(self, seed: int) -> None:
        self.seed: int = seed
        self.chunks: Dict[Tuple[int, int, int], Chunk] = {}
        self.day_time: float = 0.5  # start at noon
        self.time_speed: float = 1.0 / 1200.0  # full cycle = 1200 seconds by default

    # ------------------------------------------------------------------
    # Coordinate helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _world_to_chunk(x: int, y: int, z: int) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """Return (chunk_coords, local_coords) for world position (x, y, z)."""
        cx = math.floor(x / CHUNK_SIZE)
        cy = math.floor(y / CHUNK_SIZE)
        cz = math.floor(z / CHUNK_SIZE)
        lx = x - cx * CHUNK_SIZE
        ly = y - cy * CHUNK_SIZE
        lz = z - cz * CHUNK_SIZE
        return (cx, cy, cz), (lx, ly, lz)

    # ------------------------------------------------------------------
    # Chunk management
    # ------------------------------------------------------------------

    def get_chunk(self, cx: int, cy: int, cz: int) -> Chunk:
        """Return (and generate if needed) the chunk at chunk coords."""
        key = (cx, cy, cz)
        if key not in self.chunks:
            self.chunks[key] = self._generate_chunk(cx, cy, cz)
        return self.chunks[key]

    def _generate_chunk(self, cx: int, cy: int, cz: int) -> Chunk:
        """Procedurally generate a new chunk at chunk coordinates (cx, cy, cz)."""
        chunk = Chunk(position=(cx, cy, cz))
        base_x = cx * CHUNK_SIZE
        base_y = cy * CHUNK_SIZE
        base_z = cz * CHUNK_SIZE

        for lx in range(CHUNK_SIZE):
            for lz in range(CHUNK_SIZE):
                wx = base_x + lx
                wz = base_z + lz
                surface = _terrain_height(self.seed, wx, wz)
                for ly in range(CHUNK_SIZE):
                    wy = base_y + ly
                    if wy > surface:
                        block = BlockType.AIR
                    elif wy == surface:
                        block = BlockType.GRASS
                    elif wy >= surface - 3:
                        block = BlockType.DIRT
                    else:
                        block = BlockType.STONE
                    if block != BlockType.AIR:
                        chunk.blocks[(lx, ly, lz)] = block

        chunk.is_dirty = True
        return chunk

    def load_chunks_around(self, position: tuple, radius: int) -> None:
        """Ensure all chunks within *radius* of the player's chunk are loaded."""
        px, py, pz = int(position[0]), int(position[1]), int(position[2])
        cx0 = math.floor(px / CHUNK_SIZE)
        cy0 = math.floor(py / CHUNK_SIZE)
        cz0 = math.floor(pz / CHUNK_SIZE)
        for dx in range(-radius, radius + 1):
            for dy in range(-1, 2):
                for dz in range(-radius, radius + 1):
                    self.get_chunk(cx0 + dx, cy0 + dy, cz0 + dz)

    # ------------------------------------------------------------------
    # Block access
    # ------------------------------------------------------------------

    def get_block(self, x: int, y: int, z: int) -> BlockType:
        chunk_coords, local_coords = self._world_to_chunk(x, y, z)
        chunk = self.get_chunk(*chunk_coords)
        return chunk.get_block(*local_coords)

    def set_block(self, x: int, y: int, z: int, block_type: BlockType) -> None:
        chunk_coords, local_coords = self._world_to_chunk(x, y, z)
        chunk = self.get_chunk(*chunk_coords)
        chunk.set_block(*local_coords, block_type)

    def break_block(self, x: int, y: int, z: int) -> Optional[ItemType]:
        """Break the block at (x, y, z). Returns the dropped ItemType or None."""
        current = self.get_block(x, y, z)
        if current == BlockType.AIR:
            return None
        props = get_block_properties(current)
        self.set_block(x, y, z, BlockType.AIR)
        if props.drop is not None:
            try:
                return ItemType[props.drop]
            except KeyError:
                return None
        return None

    def place_block(self, x: int, y: int, z: int, block_type: BlockType) -> bool:
        """Place a block at (x, y, z). Returns False if the space is occupied."""
        if self.get_block(x, y, z) != BlockType.AIR:
            return False
        self.set_block(x, y, z, block_type)
        return True

    # ------------------------------------------------------------------
    # World update (day/night cycle)
    # ------------------------------------------------------------------

    def update(self, dt: float) -> None:
        """Advance the day/night cycle by dt seconds."""
        self.day_time = (self.day_time + self.time_speed * dt) % 1.0

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def to_save_data(self) -> dict:
        """Serialise only chunks that contain player-modified blocks."""
        modified: dict = {}
        for (cx, cy, cz), chunk in self.chunks.items():
            if chunk.blocks:
                key = f"{cx},{cy},{cz}"
                blocks_serialised = {
                    f"{lx},{ly},{lz}": bt.name
                    for (lx, ly, lz), bt in chunk.blocks.items()
                }
                modified[key] = {"blocks": blocks_serialised}
        return {"modified_chunks": modified}

    def from_save_data(self, data: dict) -> None:
        """Restore chunk data from a saved dict."""
        self.chunks.clear()
        for key, chunk_data in data.get("modified_chunks", {}).items():
            cx, cy, cz = (int(v) for v in key.split(","))
            chunk = Chunk(position=(cx, cy, cz))
            for bkey, bname in chunk_data.get("blocks", {}).items():
                lx, ly, lz = (int(v) for v in bkey.split(","))
                chunk.blocks[(lx, ly, lz)] = BlockType[bname]
            chunk.is_dirty = True
            self.chunks[(cx, cy, cz)] = chunk

    @property
    def is_night(self) -> bool:
        """Return True if day_time indicates night (outside 0.25–0.75 window)."""
        return self.day_time < 0.25 or self.day_time > 0.75
