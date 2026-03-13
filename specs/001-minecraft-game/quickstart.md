# Quickstart Guide: Minecraft-Like Sandbox Game

**Feature**: 001-minecraft-game  
**Date**: 2026-03-13

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
# Clone or navigate to the repository
cd /path/to/vibe2

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate.bat     # Windows

# Install dependencies
pip install -r requirements.txt
```

## requirements.txt

```text
ursina>=6.0.0
noise>=1.2.2
pytest>=7.0.0
pytest-mock>=3.0.0
```

## Running the Game

```bash
# From repository root with virtual environment active
python src/main.py
```

## Controls

| Action | Key/Button |
|--------|-----------|
| Move forward/back/left/right | W / S / A / D |
| Jump | Space |
| Look around | Mouse movement |
| Break block | Left Mouse Button (hold) |
| Place block | Right Mouse Button |
| Open crafting | E |
| Hotbar select | 1–9 or Mouse Scroll |
| Save game | F5 |
| Pause / Main Menu | Escape |

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/unit/
pytest tests/integration/

# Run with verbose output
pytest -v tests/
```

## Development Workflow

```
1. spec.md     → Feature requirements (speckit.specify)
2. plan.md     → This plan (speckit.plan)
3. tasks.md    → Implementation tasks (speckit.tasks)
4. src/        → Implementation (TDD: write tests first)
5. tests/      → Test suite
```

## Project Layout

```
vibe2/
├── src/                    # Game source code
│   ├── main.py             # Entry point
│   ├── world/              # World, chunks, blocks
│   ├── player/             # Player, inventory, health
│   ├── entities/           # Enemies, item drops
│   ├── crafting/           # Recipes, crafting UI
│   ├── ui/                 # HUD, main menu
│   └── persistence/        # Save/load
├── tests/                  # Test suite (pytest)
│   ├── unit/
│   ├── integration/
│   └── contract/
├── saves/                  # Save files (auto-created)
├── assets/                 # Textures, sounds
├── specs/001-minecraft-game/  # Spec and design docs
└── requirements.txt
```
