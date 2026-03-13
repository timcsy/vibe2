"""Main entry point for the Minecraft-like sandbox game.

Run with:
    python src/main.py

Requires the Ursina game engine (pip install ursina>=6.0.0).
"""
from __future__ import annotations

import json
import os
import sys

# ---------------------------------------------------------------------------
# Ursina availability guard — allow unit tests to import this module
# ---------------------------------------------------------------------------
try:
    from ursina import (  # type: ignore
        Ursina, Entity, FirstPersonController, Sky, color,
        raycast, mouse, held_keys, time, application, Vec3,
        window, Text, camera,
    )
    from ursina.prefabs.first_person_controller import FirstPersonController  # type: ignore
    URSINA_AVAILABLE = True
except ImportError:  # pragma: no cover
    URSINA_AVAILABLE = False

from src.world.world import World
from src.world.block import BlockType, get_block_properties
from src.player.player import Player
from src.player.inventory import ItemType
from src.entities.enemy import Enemy, EnemyType, EnemyState
from src.entities.item_drop import ItemDrop
from src.crafting.recipe import build_default_registry
from src.crafting.crafting_ui import CraftingUI
from src.ui.hud import HUD
from src.ui.main_menu import MainMenu, MenuAction
from src.persistence.save_manager import SaveManager

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
try:
    with open(_CONFIG_PATH) as _f:
        _CONFIG = json.load(_f)
except Exception:
    _CONFIG = {}

AUTO_SAVE_INTERVAL: float = float(_CONFIG.get("auto_save_interval_seconds", 300))
CHUNK_RENDER_RADIUS: int = int(_CONFIG.get("chunk_render_radius", 4))
DAY_CYCLE_SECONDS: float = float(_CONFIG.get("day_cycle_seconds", 1200))

# Block texture colour palette (fallback if texture files absent)
BLOCK_COLORS: dict[BlockType, tuple] = {
    BlockType.GRASS:          (0.3, 0.7, 0.3),
    BlockType.DIRT:           (0.5, 0.3, 0.1),
    BlockType.STONE:          (0.5, 0.5, 0.5),
    BlockType.WOOD:           (0.6, 0.4, 0.2),
    BlockType.LEAVES:         (0.1, 0.6, 0.1),
    BlockType.WATER:          (0.2, 0.4, 0.8),
    BlockType.SAND:           (0.9, 0.8, 0.5),
    BlockType.ORE_COAL:       (0.3, 0.3, 0.3),
    BlockType.ORE_IRON:       (0.7, 0.5, 0.4),
    BlockType.CRAFTING_TABLE: (0.7, 0.5, 0.2),
    BlockType.CHEST:          (0.8, 0.6, 0.2),
}


# ---------------------------------------------------------------------------
# Game state (module-level so Ursina update() can access it)
# ---------------------------------------------------------------------------
_world: World | None = None
_player_logic: Player | None = None
_ursina_player: object | None = None
_hud: HUD | None = None
_crafting_ui: CraftingUI | None = None
_item_drops: list[ItemDrop] = []
_enemies: list[Enemy] = []
_block_entities: dict[tuple, object] = {}
_save_manager: SaveManager | None = None
_auto_save_timer: float = 0.0
_current_save_name: str = "world"


def _spawn_block_entity(x: int, y: int, z: int, block_type: BlockType) -> None:
    """Create a visible Ursina block entity."""
    if not URSINA_AVAILABLE:
        return
    col = BLOCK_COLORS.get(block_type, (1, 1, 1))
    entity = Entity(
        model="cube",
        color=color.rgb(*[int(c * 255) for c in col]),
        position=(x, y, z),
        collider="box",
    )
    _block_entities[(x, y, z)] = entity


def _remove_block_entity(x: int, y: int, z: int) -> None:
    if not URSINA_AVAILABLE:
        return
    entity = _block_entities.pop((x, y, z), None)
    if entity is not None:
        entity.disable()


def _load_visible_chunks() -> None:
    if _world is None or _ursina_player is None:
        return
    pos = _ursina_player.position  # type: ignore[attr-defined]
    _world.load_chunks_around((pos.x, pos.y, pos.z), CHUNK_RENDER_RADIUS)
    for (cx, cy, cz), chunk in _world.chunks.items():
        if not chunk.is_dirty:
            continue
        for (lx, ly, lz), bt in chunk.blocks.items():
            wx = cx * 16 + lx
            wy = cy * 16 + ly
            wz = cz * 16 + lz
            key = (wx, wy, wz)
            if key not in _block_entities and bt != BlockType.AIR:
                _spawn_block_entity(wx, wy, wz, bt)
        chunk.is_dirty = False


def input(key: str) -> None:  # noqa: A001  (Ursina callback name)
    global _auto_save_timer
    if _world is None or _player_logic is None:
        return

    if key == "left mouse button":
        # Break targeted block
        hit = raycast(
            camera.world_position,  # type: ignore[name-defined]
            camera.forward,  # type: ignore[name-defined]
            distance=_player_logic.reach,
            ignore=[_ursina_player],
        )
        if hit.hit:
            pos = hit.entity.position
            x, y, z = int(pos.x), int(pos.y), int(pos.z)
            drop = _world.break_block(x, y, z)
            _remove_block_entity(x, y, z)
            if drop is not None:
                _item_drops.append(ItemDrop((x + 0.5, y + 0.5, z + 0.5), drop))
                _player_logic.inventory.add_item(drop)

    elif key == "right mouse button":
        # Place block
        hit = raycast(
            camera.world_position,  # type: ignore[name-defined]
            camera.forward,  # type: ignore[name-defined]
            distance=_player_logic.reach,
            ignore=[_ursina_player],
        )
        if hit.hit:
            selected = _player_logic.inventory.get_selected_item()
            if selected is not None:
                try:
                    bt = BlockType[selected.item_type.name]
                    pos = hit.entity.position + hit.normal
                    x, y, z = int(pos.x), int(pos.y), int(pos.z)
                    if _world.place_block(x, y, z, bt):
                        _player_logic.inventory.remove_item(selected.item_type)
                        _spawn_block_entity(x, y, z, bt)
                except KeyError:
                    pass

    elif key == "e":
        if _crafting_ui is not None:
            _crafting_ui.toggle()

    elif key == "f5":
        if _save_manager is not None and _world is not None and _player_logic is not None:
            _save_manager.save(_world, _player_logic, _current_save_name)

    elif key in "123456789":
        slot = int(key) - 1
        _player_logic.selected_slot = slot
        if _hud is not None:
            _hud.select_slot(slot)

    elif key == "scroll up":
        if _player_logic is not None and _hud is not None:
            _player_logic.selected_slot = _hud.scroll_hotbar(-1)

    elif key == "scroll down":
        if _player_logic is not None and _hud is not None:
            _player_logic.selected_slot = _hud.scroll_hotbar(1)


def update() -> None:  # noqa: A001  (Ursina callback name)
    global _auto_save_timer
    if _world is None or _player_logic is None or _ursina_player is None:
        return

    dt: float = time.dt  # type: ignore[attr-defined]

    # Sync logic player position from Ursina controller
    pos = _ursina_player.position  # type: ignore[attr-defined]
    _player_logic.position = (pos.x, pos.y, pos.z)

    # World update (day/night cycle)
    _world.update(dt)

    # HUD update
    if _hud is not None:
        _hud.update(_player_logic, dt)

    # Load chunks around player
    _load_visible_chunks()

    # Enemy updates
    for enemy in list(_enemies):
        if not enemy.is_alive():
            continue
        enemy.update(_player_logic.position, dt, _world.is_night)
        if enemy.state == EnemyState.ATTACK:
            dmg = enemy.get_attack_damage() * dt
            _player_logic.take_damage(dmg)
            if _hud is not None:
                _hud.trigger_damage_flash()

    # Item drop updates
    for drop in list(_item_drops):
        drop.update(_player_logic, dt)

    # Auto-save
    _auto_save_timer += dt
    if _auto_save_timer >= AUTO_SAVE_INTERVAL and _save_manager is not None:
        _save_manager.auto_save(_world, _player_logic)
        _auto_save_timer = 0.0

    # Respawn on death
    if not _player_logic.is_alive():
        _player_logic.respawn()
        if URSINA_AVAILABLE:
            _ursina_player.position = Vec3(*_player_logic.position)  # type: ignore[attr-defined]


def _start_new_game(seed: int = 42) -> None:
    global _world, _player_logic, _ursina_player, _hud, _crafting_ui, _save_manager

    _world = World(seed=seed)
    _world.time_speed = 1.0 / DAY_CYCLE_SECONDS
    _player_logic = Player()
    _hud = HUD()
    registry = build_default_registry()
    _crafting_ui = CraftingUI(registry)
    _save_manager = SaveManager()

    # Initial chunk load
    _world.load_chunks_around(_player_logic.position, CHUNK_RENDER_RADIUS)

    if URSINA_AVAILABLE:
        _ursina_player = FirstPersonController(  # type: ignore[name-defined]
            position=Vec3(*_player_logic.position),  # type: ignore[name-defined]
        )
        Sky()  # type: ignore[name-defined]
        _load_visible_chunks()


def _start_from_save(save_name: str) -> None:
    global _world, _player_logic, _ursina_player, _hud, _crafting_ui, _save_manager

    _save_manager = SaveManager()
    world_save = _save_manager.load(save_name)
    if world_save is None:
        _start_new_game()
        return

    _world = World(seed=world_save.seed)
    _world.day_time = world_save.day_time
    _world.time_speed = 1.0 / DAY_CYCLE_SECONDS
    _world.from_save_data({"modified_chunks": world_save.modified_chunks})

    _player_logic = Player(
        position=tuple(world_save.player_position),  # type: ignore[arg-type]
        max_health=20.0,
    )
    _player_logic.health = world_save.player_health
    _player_logic.inventory.from_dict(world_save.player_inventory)

    _hud = HUD()
    registry = build_default_registry()
    _crafting_ui = CraftingUI(registry)

    if URSINA_AVAILABLE:
        _ursina_player = FirstPersonController(  # type: ignore[name-defined]
            position=Vec3(*_player_logic.position),  # type: ignore[name-defined]
        )
        Sky()  # type: ignore[name-defined]
        _load_visible_chunks()


def main() -> None:
    if not URSINA_AVAILABLE:
        print("Ursina engine not installed. Run: pip install ursina>=6.0.0")
        sys.exit(1)

    app = Ursina()  # type: ignore[name-defined]
    window.title = "Voxel Sandbox"  # type: ignore[attr-defined]

    save_manager = SaveManager()
    saves = save_manager.list_saves()
    menu = MainMenu(available_saves=saves)

    if saves:
        menu_entity = Text(  # type: ignore[name-defined]
            text="Press N for New Game, L to Load last save, Q to quit",
            origin=(0, 0),
            scale=2,
        )
        # Simple immediate decision via command line args for headless launches
        if len(sys.argv) > 1 and sys.argv[1] == "--load" and len(sys.argv) > 2:
            menu.load_game(sys.argv[2])
        else:
            menu.new_game()
    else:
        menu.new_game()

    if menu.pending_action == MenuAction.NEW_GAME:
        _start_new_game()
    elif menu.pending_action == MenuAction.LOAD_GAME:
        _start_from_save(menu.selected_save)

    app.run()


if __name__ == "__main__":
    main()
