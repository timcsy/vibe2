# Game API Contract: Minecraft-Like Sandbox Game

**Feature**: 001-minecraft-game  
**Phase**: 1 - Design  
**Date**: 2026-03-13

This document defines the internal module contracts — the interfaces between game subsystems. These are the Python class/function signatures that each module must honour.

---

## World Module (`src/world/world.py`)

```python
class World:
    def __init__(self, seed: int) -> None: ...
    def get_block(self, x: int, y: int, z: int) -> BlockType: ...
    def set_block(self, x: int, y: int, z: int, block_type: BlockType) -> None: ...
    def break_block(self, x: int, y: int, z: int) -> Optional[ItemType]: ...
    def place_block(self, x: int, y: int, z: int, block_type: BlockType) -> bool: ...
    def get_chunk(self, cx: int, cy: int, cz: int) -> Chunk: ...
    def load_chunks_around(self, position: Vec3, radius: int) -> None: ...
    def update(self, dt: float) -> None:  # advances day/night cycle
```

---

## Player Module (`src/player/player.py`)

```python
class Player:
    health: float
    max_health: float
    inventory: Inventory
    position: Vec3

    def move(self, direction: Vec3, dt: float) -> None: ...
    def jump(self) -> None: ...
    def break_targeted_block(self, world: World) -> None: ...
    def place_block(self, world: World) -> None: ...
    def take_damage(self, amount: float) -> None: ...
    def heal(self, amount: float) -> None: ...
    def is_alive(self) -> bool: ...
    def respawn(self, spawn_position: Vec3) -> None: ...
```

---

## Inventory Module (`src/player/inventory.py`)

```python
class Inventory:
    slots: List[Optional[ItemStack]]
    max_slots: int

    def add_item(self, item_type: ItemType, quantity: int = 1) -> bool: ...
        # Returns True if added, False if inventory full
    def remove_item(self, item_type: ItemType, quantity: int = 1) -> bool: ...
        # Returns True if removed, False if insufficient
    def has_items(self, item_type: ItemType, quantity: int) -> bool: ...
    def get_hotbar(self) -> List[Optional[ItemStack]]: ...
    def get_selected_item(self) -> Optional[ItemStack]: ...
    def to_dict(self) -> List[dict]: ...       # for serialization
    def from_dict(self, data: List[dict]) -> None: ...  # for deserialization
```

---

## Crafting Module (`src/crafting/recipe.py`)

```python
class RecipeRegistry:
    def register(self, pattern: List[List[Optional[ItemType]]], 
                 result: ItemType, count: int = 1) -> None: ...
    def find_recipe(self, grid: List[List[Optional[ItemType]]]) -> Optional[Recipe]: ...
    def get_all_recipes(self) -> List[Recipe]: ...

def craft(registry: RecipeRegistry, 
          grid: List[List[Optional[ItemType]]], 
          inventory: Inventory) -> Optional[ItemType]:
    # Returns crafted item type or None if no valid recipe / insufficient materials
```

---

## Enemy Module (`src/entities/enemy.py`)

```python
class Enemy:
    position: Vec3
    health: float
    state: EnemyState
    enemy_type: EnemyType

    def update(self, player_position: Vec3, dt: float, is_night: bool) -> None: ...
    def take_damage(self, amount: float) -> Optional[List[Tuple[ItemType, int]]]: ...
        # Returns item drops when killed, None otherwise
    def is_alive(self) -> bool: ...
    def get_attack_damage(self) -> float: ...
```

---

## Save Manager (`src/persistence/save_manager.py`)

```python
class SaveManager:
    def save(self, world: World, player: Player, save_name: str) -> bool: ...
    def load(self, save_name: str) -> Optional[WorldSave]: ...
    def list_saves(self) -> List[str]: ...
    def delete_save(self, save_name: str) -> bool: ...
    def auto_save(self, world: World, player: Player) -> None: ...
```
