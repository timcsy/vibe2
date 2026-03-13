# Save Format Contract: Minecraft-Like Sandbox Game

**Feature**: 001-minecraft-game  
**Phase**: 1 - Design  
**Date**: 2026-03-13

## Overview

Save files are stored in `saves/` directory relative to the game executable. Each save consists of:

- `saves/{name}/metadata.json` — Human-readable game metadata
- `saves/{name}/world.pkl` — Binary-encoded chunk block data (pickle)

## metadata.json Schema

```json
{
  "version": "1.0",
  "save_name": "string",
  "save_timestamp": "ISO 8601 datetime string",
  "seed": "integer",
  "day_time": "float (0.0–1.0)",
  "player": {
    "position": [0.0, 0.0, 0.0],
    "health": 20.0,
    "inventory": [
      {
        "slot": 0,
        "item_type": "WOOD",
        "quantity": 5
      }
    ]
  }
}
```

## world.pkl Structure

The pickle file contains a dictionary:

```python
{
    "modified_chunks": {
        "0,0,0": {          # chunk coord key "cx,cy,cz"
            "blocks": {
                "0,63,0": "GRASS",   # local block coord "x,y,z" → BlockType name
                "0,62,0": "DIRT",
                # ... only non-default blocks stored (sparse)
            }
        }
    }
}
```

## Versioning

- Save format `version` field is compared on load
- If version mismatch, a migration warning is shown
- Current version: `"1.0"`

## Auto-save

Auto-save writes to `saves/{name}_autosave/` following the same format. Auto-save interval: 5 minutes (configurable via `config.json`).
