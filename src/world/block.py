from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class BlockType(Enum):
    AIR = auto()
    GRASS = auto()
    DIRT = auto()
    STONE = auto()
    WOOD = auto()
    LEAVES = auto()
    WATER = auto()
    SAND = auto()
    ORE_COAL = auto()
    ORE_IRON = auto()
    CRAFTING_TABLE = auto()
    CHEST = auto()


@dataclass(frozen=True)
class BlockProperties:
    hardness: float
    drop: Optional[str]   # ItemType name; str to avoid circular import
    is_solid: bool
    texture: str


# Static block property registry
BLOCK_PROPERTIES: dict[BlockType, BlockProperties] = {
    BlockType.AIR:            BlockProperties(hardness=0.0,  drop=None,             is_solid=False, texture="air"),
    BlockType.GRASS:          BlockProperties(hardness=0.5,  drop="DIRT",           is_solid=True,  texture="grass"),
    BlockType.DIRT:           BlockProperties(hardness=0.5,  drop="DIRT",           is_solid=True,  texture="dirt"),
    BlockType.STONE:          BlockProperties(hardness=1.5,  drop="STONE",          is_solid=True,  texture="stone"),
    BlockType.WOOD:           BlockProperties(hardness=2.0,  drop="WOOD",           is_solid=True,  texture="wood"),
    BlockType.LEAVES:         BlockProperties(hardness=0.2,  drop=None,             is_solid=False, texture="leaves"),
    BlockType.WATER:          BlockProperties(hardness=0.0,  drop=None,             is_solid=False, texture="water"),
    BlockType.SAND:           BlockProperties(hardness=0.5,  drop="SAND",           is_solid=True,  texture="sand"),
    BlockType.ORE_COAL:       BlockProperties(hardness=3.0,  drop="COAL",           is_solid=True,  texture="ore_coal"),
    BlockType.ORE_IRON:       BlockProperties(hardness=3.0,  drop="IRON_ORE",       is_solid=True,  texture="ore_iron"),
    BlockType.CRAFTING_TABLE: BlockProperties(hardness=2.5,  drop="CRAFTING_TABLE", is_solid=True,  texture="crafting_table"),
    BlockType.CHEST:          BlockProperties(hardness=2.5,  drop=None,             is_solid=True,  texture="chest"),
}


def get_block_properties(block_type: BlockType) -> BlockProperties:
    return BLOCK_PROPERTIES[block_type]
