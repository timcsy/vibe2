"""Save/load world and player state to disk."""
from __future__ import annotations

import json
import os
import pickle
from datetime import datetime, timezone

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.world.world import World
    from src.player.player import Player

SAVES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "saves")
SAVE_FORMAT_VERSION = "1.0"


class WorldSave:
    def __init__(self, data: dict) -> None:
        self.version: str = data.get("version", SAVE_FORMAT_VERSION)
        self.save_name: str = data.get("save_name", "")
        self.save_timestamp: str = data.get("save_timestamp", "")
        self.seed: int = data.get("seed", 0)
        self.day_time: float = data.get("day_time", 0.5)
        self.player_position: List[float] = data.get("player", {}).get("position", [0.0, 70.0, 0.0])
        self.player_health: float = data.get("player", {}).get("health", 20.0)
        self.player_inventory: List[dict] = data.get("player", {}).get("inventory", [])
        self.modified_chunks: dict = data.get("modified_chunks", {})


class SaveManager:
    def __init__(self, saves_dir: str = SAVES_DIR) -> None:
        self.saves_dir = saves_dir
        os.makedirs(self.saves_dir, exist_ok=True)

    def _save_path(self, save_name: str) -> str:
        return os.path.join(self.saves_dir, save_name)

    def save(self, world: "World", player: "Player", save_name: str) -> bool:
        """Write metadata.json and world.pkl to saves/{save_name}/."""
        try:
            save_dir = self._save_path(save_name)
            os.makedirs(save_dir, exist_ok=True)

            metadata = {
                "version": SAVE_FORMAT_VERSION,
                "save_name": save_name,
                "save_timestamp": datetime.now(timezone.utc).isoformat(),
                "seed": world.seed,
                "day_time": world.day_time,
                "player": {
                    "position": list(player.position),
                    "health": player.health,
                    "inventory": player.inventory.to_dict(),
                },
            }
            with open(os.path.join(save_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f, indent=2)

            world_data = world.to_save_data()
            with open(os.path.join(save_dir, "world.pkl"), "wb") as f:
                pickle.dump(world_data, f)

            return True
        except Exception:
            return False

    def load(self, save_name: str) -> Optional[WorldSave]:
        """Load a save and return a WorldSave object, or None if not found."""
        save_dir = self._save_path(save_name)
        meta_path = os.path.join(save_dir, "metadata.json")
        world_path = os.path.join(save_dir, "world.pkl")
        if not os.path.exists(meta_path):
            return None
        try:
            with open(meta_path) as f:
                metadata = json.load(f)
            if os.path.exists(world_path):
                with open(world_path, "rb") as f:
                    world_data = pickle.load(f)
                metadata["modified_chunks"] = world_data.get("modified_chunks", {})
            return WorldSave(metadata)
        except Exception:
            return None

    def list_saves(self) -> List[str]:
        """Return a list of available save names."""
        try:
            return [
                d for d in os.listdir(self.saves_dir)
                if os.path.isdir(os.path.join(self.saves_dir, d))
            ]
        except FileNotFoundError:
            return []

    def delete_save(self, save_name: str) -> bool:
        """Delete a save directory. Returns True if deleted, False if not found."""
        import shutil
        save_dir = self._save_path(save_name)
        if not os.path.exists(save_dir):
            return False
        try:
            shutil.rmtree(save_dir)
            return True
        except Exception:
            return False

    def auto_save(self, world: "World", player: "Player") -> None:
        """Write an auto-save slot."""
        self.save(world, player, f"{getattr(world, '_save_name', 'world')}_autosave")
