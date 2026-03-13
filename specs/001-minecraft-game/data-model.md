# Data Model: Minecraft-Like Sandbox Game

**Feature**: 001-minecraft-game  
**Phase**: 1 - Design  
**Date**: 2026-03-13

## Entities

### World

The 3D voxel environment composed of chunks.

| Field | Type | Description |
|-------|------|-------------|
| `seed` | `int` | Procedural generation seed |
| `chunks` | `Dict[Tuple[int,int,int], Chunk]` | Loaded chunk map keyed by chunk coords |
| `day_time` | `float` | Current time of day (0.0–1.0, where 0.5 = noon) |
| `time_speed` | `float` | Rate of day/night progression |

**Relationships**: World contains many Chunks; World has one Player; World has many Enemies.

**State Transitions**:
- `day_time` cycles 0.0 → 1.0 → 0.0 continuously
- Chunks are loaded on demand as player moves, unloaded when far away

---

### Chunk

A 16×16×16 section of the world.

| Field | Type | Description |
|-------|------|-------------|
| `position` | `Tuple[int,int,int]` | Chunk coordinates (not block coordinates) |
| `blocks` | `Dict[Tuple[int,int,int], BlockType]` | Block type at each local position |
| `is_dirty` | `bool` | True if mesh needs to be rebuilt |
| `is_loaded` | `bool` | True if chunk mesh is active |

**Validation Rules**:
- Block positions are within `(0,0,0)` to `(15,15,15)` locally
- Air blocks can be omitted from the dict (sparse representation)

---

### Block

The fundamental building unit; represented as an enum of types.

| Field | Type | Description |
|-------|------|-------------|
| `block_type` | `BlockType` (enum) | Type of block |
| `hardness` | `float` | Time in seconds to break with bare hands |
| `drop` | `ItemType` | Item dropped when broken |
| `is_solid` | `bool` | Whether block is collidable |
| `texture` | `str` | Texture name for rendering |

**Block Types**: `AIR`, `GRASS`, `DIRT`, `STONE`, `WOOD`, `LEAVES`, `WATER`, `SAND`, `ORE_COAL`, `ORE_IRON`, `CRAFTING_TABLE`, `CHEST`

---

### Player

The user-controlled character.

| Field | Type | Description |
|-------|------|-------------|
| `position` | `Vec3` | World position (x, y, z) |
| `rotation` | `Vec3` | Camera orientation (pitch, yaw, roll) |
| `health` | `float` | Current health (0.0–20.0) |
| `max_health` | `float` | Maximum health (default 20.0) |
| `inventory` | `Inventory` | Player's inventory |
| `selected_slot` | `int` | Currently selected hotbar slot (0–8) |
| `reach` | `float` | Block interaction range in world units |

**State Transitions**:
- `Alive` → `Dead` when `health ≤ 0`
- `Dead` → `Alive` when player chooses to respawn

---

### Inventory

A container of item stacks with a maximum capacity.

| Field | Type | Description |
|-------|------|-------------|
| `slots` | `List[Optional[ItemStack]]` | Item stacks, None = empty |
| `max_slots` | `int` | Maximum number of slots (default 36) |
| `hotbar_size` | `int` | Number of hotbar slots (default 9) |

**Validation Rules**:
- `len(slots) == max_slots` always
- `ItemStack.quantity > 0` always (remove stack when quantity reaches 0)
- Cannot add items when all slots are full

**Operations**: `add_item(item_type, qty)`, `remove_item(item_type, qty)`, `get_hotbar()`, `equip(slot)`

---

### ItemStack

A quantity of a specific item type.

| Field | Type | Description |
|-------|------|-------------|
| `item_type` | `ItemType` (enum) | Type of item |
| `quantity` | `int` | Number of items in stack (≥1) |
| `max_stack` | `int` | Maximum stack size for this item type |

**Item Types**: `WOOD`, `STICK`, `STONE`, `COAL`, `IRON_ORE`, `IRON_INGOT`, `WOOD_PLANKS`, `WOOD_PICKAXE`, `STONE_PICKAXE`, `IRON_PICKAXE`, `WOOD_SWORD`, `STONE_SWORD`, `IRON_SWORD`, `TORCH`, `CRAFTING_TABLE`

---

### Recipe

Defines a crafting transformation.

| Field | Type | Description |
|-------|------|-------------|
| `pattern` | `List[List[Optional[ItemType]]]` | 3×3 grid of input items (None = empty) |
| `result` | `ItemType` | Output item type |
| `result_count` | `int` | Number of output items |

**Validation Rules**:
- `pattern` is always a 3×3 matrix
- `result_count ≥ 1`

---

### Enemy

A hostile non-player character.

| Field | Type | Description |
|-------|------|-------------|
| `position` | `Vec3` | World position |
| `health` | `float` | Current health |
| `max_health` | `float` | Maximum health |
| `damage` | `float` | Damage dealt per attack |
| `detection_range` | `float` | Distance at which enemy detects player |
| `attack_range` | `float` | Distance at which enemy can attack |
| `attack_cooldown` | `float` | Seconds between attacks |
| `enemy_type` | `EnemyType` (enum) | Type of enemy (`ZOMBIE`, `SKELETON`) |
| `state` | `EnemyState` (enum) | AI state |

**Enemy States**: `IDLE`, `ALERT`, `CHASE`, `ATTACK`, `DEAD`

**State Transitions**:
```
IDLE → ALERT: player enters detection_range at night
ALERT → CHASE: confirmed player detection
CHASE → ATTACK: player enters attack_range
ATTACK → CHASE: attack_cooldown elapsed, player out of attack_range
CHASE → IDLE: player leaves detection_range or daytime
* → DEAD: health ≤ 0
```

---

### WorldSave

Snapshot of complete game state for persistence.

| Field | Type | Description |
|-------|------|-------------|
| `version` | `str` | Save format version (e.g., "1.0") |
| `seed` | `int` | World generation seed |
| `player_position` | `List[float]` | [x, y, z] |
| `player_health` | `float` | Player health at save time |
| `player_inventory` | `List[dict]` | Serialized inventory slots |
| `modified_chunks` | `Dict[str, dict]` | Chunks with player-made changes (key: "x,y,z") |
| `day_time` | `float` | Time of day at save time |
| `save_timestamp` | `str` | ISO 8601 save datetime |

---

## Entity Relationships

```
World
 ├── has many → Chunk
 ├── has one  → Player
 │              └── has one → Inventory
 │                            └── has many → ItemStack
 ├── has many → Enemy
 └── references → WorldSave (for persistence)

Recipe (static registry, no instance ownership)
Block (static definitions via BlockType enum)
```
