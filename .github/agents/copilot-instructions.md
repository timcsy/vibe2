# Minecraft-Like Sandbox Game Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-13

## Active Technologies

- **Language**: Python 3.11
- **Game Engine**: Ursina Engine 6.x (built on Panda3D)
- **Noise Generation**: noise 1.2.x (Perlin/Simplex noise for world generation)
- **Testing**: pytest 7.x + pytest-mock
- **Serialization**: json + pickle (stdlib)
- **Package Management**: pip + requirements.txt

## Project Structure

```text
src/
├── world/
│   ├── chunk.py         # Chunk data and mesh
│   ├── world.py         # World manager, procedural gen
│   └── block.py         # Block types and properties
├── player/
│   ├── player.py        # Player controller (movement, physics)
│   ├── inventory.py     # Inventory management
│   └── health.py        # Health system
├── entities/
│   ├── enemy.py         # Enemy AI and behavior
│   └── item_drop.py     # Dropped item entities
├── crafting/
│   ├── recipe.py        # Recipe definitions
│   └── crafting_ui.py   # Crafting interface
├── ui/
│   ├── hud.py           # HUD (health bar, hotbar)
│   └── main_menu.py     # Main menu
├── persistence/
│   └── save_manager.py  # Save/load world state
└── main.py              # Entry point

tests/
├── unit/
│   ├── test_world.py
│   ├── test_inventory.py
│   ├── test_crafting.py
│   ├── test_health.py
│   └── test_save_manager.py
├── integration/
│   └── test_gameplay.py
└── contract/
    └── test_save_format.py
```

## Commands

```bash
# Setup
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt

# Run game
python src/main.py

# Run tests
pytest tests/
pytest tests/unit/
pytest tests/integration/
pytest -v tests/
```

## Code Style

- Python 3.11 with type hints throughout
- Game logic separated from Ursina rendering for testability
- Pure Python modules (inventory, crafting, save, health) must be unit-testable without the engine
- Use enums for BlockType, ItemType, EnemyType, EnemyState
- Sparse dict representation for chunk blocks (omit AIR blocks)

## Recent Changes

- **001-minecraft-game**: Initial feature — 3D sandbox voxel game with procedural world gen, block interaction, crafting, survival mechanics, day/night cycle, enemies, and save/load

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
