# Tasks: Minecraft-Like Sandbox Game

**Input**: Design documents from `/specs/001-minecraft-game/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: Test tasks are included because TDD is an explicit principle in plan.md (Constitution Principle IV). Write and verify tests FAIL before implementing each story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and directory structure

- [X] T001 Create directory structure: `src/world/`, `src/player/`, `src/entities/`, `src/crafting/`, `src/ui/`, `src/persistence/`, `tests/unit/`, `tests/integration/`, `tests/contract/`, `saves/`, `assets/textures/`
- [X] T002 Create `requirements.txt` with `ursina>=6.0.0`, `noise>=1.2.2`, `pytest>=7.0.0`, `pytest-mock>=3.0.0`
- [X] T003 [P] Create `pytest.ini` at repository root configuring `testpaths = tests` and `python_files = test_*.py`
- [X] T004 [P] Add `__init__.py` files to all `src/` packages and `tests/` sub-packages

**Checkpoint**: Project structure in place — dependencies installable via `pip install -r requirements.txt`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared enumerations and data definitions used across all user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Define `BlockType` enum (AIR, GRASS, DIRT, STONE, WOOD, LEAVES, WATER, SAND, ORE_COAL, ORE_IRON, CRAFTING_TABLE, CHEST) and `Block` properties dataclass (`hardness`, `drop`, `is_solid`, `texture`) in `src/world/block.py`
- [X] T006 [P] Define `ItemType` enum (WOOD, STICK, STONE, COAL, IRON_ORE, IRON_INGOT, WOOD_PLANKS, WOOD_PICKAXE, STONE_PICKAXE, IRON_PICKAXE, WOOD_SWORD, STONE_SWORD, IRON_SWORD, TORCH, CRAFTING_TABLE) and `ItemStack` dataclass (`item_type`, `quantity`, `max_stack`) in `src/player/inventory.py`
- [X] T007 [P] Define `EnemyType` enum (ZOMBIE, SKELETON) and `EnemyState` enum (IDLE, ALERT, CHASE, ATTACK, DEAD) in `src/entities/enemy.py`

**Checkpoint**: Foundation ready — all enums and shared types defined; user story implementation can begin

---

## Phase 3: User Story 1 — Explore and Interact with a Voxel World (Priority: P1) 🎯 MVP

**Goal**: Player can start a new game, navigate a procedurally generated 3D voxel world, and place/remove blocks.

**Independent Test**: Start a game session and verify the player can move through a generated 3D landscape, look in any direction, remove a block, and place a block — delivering a playable, navigable world.

### Tests for User Story 1 ⚠️ Write FIRST — verify they FAIL before implementing

- [X] T008 [P] [US1] Write unit tests for `Chunk` (block get/set, sparse storage, dirty flag) in `tests/unit/test_world.py`
- [X] T009 [P] [US1] Write unit tests for `World` (procedural gen seed determinism, `get_block`, `set_block`, `break_block`, `place_block`) in `tests/unit/test_world.py`

### Implementation for User Story 1

- [X] T010 [US1] Implement `Chunk` class (`position`, `blocks` dict, `is_dirty`, `is_loaded`, `get_block`, `set_block`) in `src/world/chunk.py`
- [X] T011 [US1] Implement `World` class with Perlin-noise procedural generation (`__init__`, `get_block`, `set_block`, `break_block`, `place_block`, `get_chunk`, `load_chunks_around`, `update`) in `src/world/world.py`
- [X] T012 [US1] Implement `Player` controller with movement (WASD), jump (Space), mouse-look, `break_targeted_block`, `place_block`, `take_damage`, `heal`, `is_alive`, `respawn` in `src/player/player.py`
- [X] T013 [US1] Create main entry point: initialise Ursina app, create `World` and `Player`, wire input handlers and game loop in `src/main.py`

**Checkpoint**: User Story 1 fully functional — new game starts, terrain visible, player moves, blocks break and place

---

## Phase 4: User Story 2 — Gather Resources and Craft Items (Priority: P2)

**Goal**: Player collects resource items when breaking blocks, opens a crafting interface, combines materials into tools, and equips them from inventory.

**Independent Test**: Break several block types, open the crafting interface (`E`), combine materials following a recipe, confirm the crafted item appears in inventory and can be equipped.

### Tests for User Story 2 ⚠️ Write FIRST — verify they FAIL before implementing

- [X] T014 [P] [US2] Write unit tests for `Inventory` (`add_item`, `remove_item`, `has_items`, `get_hotbar`, `get_selected_item`, `to_dict`, `from_dict`, full-inventory rejection) in `tests/unit/test_inventory.py`
- [X] T015 [P] [US2] Write unit tests for `RecipeRegistry` and `craft` function (valid recipe, insufficient materials, unknown recipe) in `tests/unit/test_crafting.py`

### Implementation for User Story 2

- [X] T016 [US2] Implement `Inventory` class (slots list, `add_item`, `remove_item`, `has_items`, `get_hotbar`, `get_selected_item`, `to_dict`, `from_dict`) per game-api.md contract in `src/player/inventory.py`
- [X] T017 [P] [US2] Implement `ItemDrop` entity (visual entity, auto-pickup on player proximity, despawn after collection) in `src/entities/item_drop.py`
- [X] T018 [P] [US2] Implement `RecipeRegistry` and `craft` function with at least 10 recipes (wood planks, sticks, pickaxes, swords, torches, crafting table) per game-api.md contract in `src/crafting/recipe.py`
- [X] T019 [US2] Implement `CraftingUI` (3×3 grid input, recipe matching display, craft button, close on `E`) in `src/crafting/crafting_ui.py`
- [X] T020 [US2] Implement HUD hotbar (9-slot display, selected-slot highlight, scroll/number-key slot cycling) in `src/ui/hud.py`
- [X] T021 [US2] Wire item drops into `World.break_block` (spawn `ItemDrop` at block position) and integrate `Inventory` into `Player` in `src/world/world.py` and `src/player/player.py`

**Checkpoint**: User Story 2 fully functional — blocks drop items, crafting interface works, items equippable from hotbar

---

## Phase 5: User Story 3 — Survive Day/Night Cycle and Enemies (Priority: P3)

**Goal**: World has a day/night cycle; hostile enemies spawn at night, pursue the player, deal damage; player can attack enemies; health system and respawn work.

**Independent Test**: Wait for nightfall, observe enemies spawn and approach, receive damage, use a weapon or shelter to survive until daytime.

### Tests for User Story 3 ⚠️ Write FIRST — verify they FAIL before implementing

- [X] T022 [P] [US3] Write unit tests for `Player` health system (`take_damage`, `heal`, death condition, `is_alive`, `respawn`) in `tests/unit/test_health.py`
- [X] T023 [P] [US3] Write unit tests for `Enemy` state-machine transitions (IDLE→ALERT→CHASE→ATTACK→DEAD, night/day toggling) in `tests/unit/test_enemy.py`

### Implementation for User Story 3

- [X] T024 [US3] Implement health module helpers (`take_damage`, `heal`, clamp to 0–max_health) used by `Player` in `src/player/health.py`
- [X] T025 [US3] Implement day/night cycle in `World.update` (`day_time` advances with `time_speed`, configurable full-cycle duration ~20 min) in `src/world/world.py`
- [X] T026 [US3] Implement `Enemy` class (state machine per data-model.md: IDLE/ALERT/CHASE/ATTACK/DEAD, `update`, `take_damage` with loot drops, `is_alive`, `get_attack_damage`) per game-api.md contract in `src/entities/enemy.py`
- [X] T027 [US3] Add HUD health bar (current/max health display, damage flash indicator) to `src/ui/hud.py`
- [X] T028 [US3] Wire enemy spawning at night, player attack (left-click on enemy), damage exchange, death/respawn flow, and world lighting change into `src/main.py`

**Checkpoint**: User Story 3 fully functional — day/night cycle visible, enemies spawn at night, combat and respawn work

---

## Phase 6: User Story 4 — Build Structures (Priority: P4)

**Goal**: Player uses collected blocks to construct multi-block buildings; structures persist across sessions; different block types are visually distinct.

**Independent Test**: Place multiple block types in consecutive positions to form a walled enclosure; verify structure persists and blocks can be removed or replaced freely.

### Tests for User Story 4 ⚠️ Write FIRST — verify they FAIL before implementing

- [X] T029 [P] [US4] Write unit tests for block placement validation in `World.place_block` (occupied-space rejection, valid adjacent placement, multiple consecutive placements) in `tests/unit/test_world.py`

### Implementation for User Story 4

- [X] T030 [US4] Ensure `Chunk.is_dirty` triggers mesh rebuild when any block is placed or removed in `src/world/chunk.py`
- [X] T031 [US4] Validate `World.place_block` rejects occupied positions and returns `False`; apply sparse block dict update in `src/world/world.py`
- [X] T032 [US4] Add block-type selection via hotbar cycling (scroll wheel, 1–9 keys) and show selected block type on HUD in `src/ui/hud.py`
- [X] T033 [US4] Ensure at least 5 distinct block textures are referenced in `Block` properties (grass, dirt, stone, wood, leaves) in `src/world/block.py`

**Checkpoint**: User Story 4 fully functional — multi-block structures build and persist; different block types visually distinct

---

## Phase 7: User Story 5 — Save and Load Game Progress (Priority: P5)

**Goal**: Player can save the world (F5), exit, relaunch, and load the saved state with all blocks, inventory, and position restored. Auto-save runs every 5 minutes.

**Independent Test**: Make world changes and inventory updates, save, exit, relaunch, load the save, and confirm all changes and position are restored.

### Tests for User Story 5 ⚠️ Write FIRST — verify they FAIL before implementing

- [X] T034 [P] [US5] Write contract test verifying `metadata.json` and `world.pkl` schema match save-format.md spec in `tests/contract/test_save_format.py`
- [X] T035 [P] [US5] Write unit tests for `SaveManager` (`save`, `load`, `list_saves`, `delete_save`, round-trip integrity) in `tests/unit/test_save_manager.py`

### Implementation for User Story 5

- [X] T036 [US5] Implement `World.to_save_data` / `World.from_save_data` serialising only modified chunks to the `WorldSave` schema in `src/world/world.py`
- [X] T037 [US5] Implement `SaveManager` (`save` writes `metadata.json` + `world.pkl`, `load` returns `WorldSave`, `list_saves`, `delete_save`, `auto_save`) per game-api.md contract and save-format.md in `src/persistence/save_manager.py`
- [X] T038 [US5] Implement main menu (`New Game`, `Load Game` list, `Quit`) using Ursina UI in `src/ui/main_menu.py`
- [X] T039 [US5] Wire `F5` manual save, save-on-quit confirmation, and 5-minute auto-save timer into `src/main.py`

**Checkpoint**: User Story 5 fully functional — save, exit, reload restores exact world state; auto-save runs on interval

---

## Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T040 [P] Create `config.json` at repository root with configurable settings (`auto_save_interval_seconds: 300`, `chunk_render_radius: 4`, `day_cycle_seconds: 1200`)
- [X] T041 [P] Add `saves/` and `.venv/` to `.gitignore`
- [X] T042 Write integration test covering full gameplay flow (world gen → move → break → craft → save → load) in `tests/integration/test_gameplay.py`
- [X] T043 [P] Audit type hints and add missing annotations across all `src/` modules
- [ ] T044 Run quickstart.md validation: install dependencies, launch game, verify 60 fps target and ≤100ms block-op response

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — **BLOCKS all user stories**
- **User Stories (Phase 3–7)**: All depend on Foundational phase completion
  - Stories can proceed sequentially in priority order (P1 → P2 → P3 → P4 → P5)
  - Or in parallel across team members once Phase 2 is done
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Phase 2 — no dependency on other stories
- **US2 (P2)**: Can start after Phase 2 — integrates with US1 (`World.break_block`, `Player.inventory`) but independently testable
- **US3 (P3)**: Can start after Phase 2 — extends `World.update` (US1) and uses `Inventory` (US2); independently testable
- **US4 (P4)**: Can start after Phase 2 — builds on `World.place_block` (US1); independently testable
- **US5 (P5)**: Can start after Phase 2 — requires `World`, `Player`, `Inventory` from US1/US2; independently testable

### Within Each User Story

1. Write tests first and confirm they FAIL
2. Implement models/data classes before services
3. Implement services before UI/integration
4. Complete and validate story before moving to next priority

### Parallel Opportunities

- All tasks marked [P] within a phase can run in parallel
- T008 and T009 can run in parallel (same file but non-overlapping test functions)
- T014 and T015 (inventory + crafting tests), T017 and T018 (ItemDrop + RecipeRegistry) are parallel pairs
- T022 and T023 (health + enemy tests), T024 and T025 (health + day-night impl) are parallel pairs
- T034 and T035 (save contract + unit tests) are a parallel pair

---

## Parallel Example: User Story 1

```bash
# Launch both test-writing tasks together (TDD phase):
Task: "Write unit tests for Chunk in tests/unit/test_world.py"  # T008
Task: "Write unit tests for World in tests/unit/test_world.py"  # T009

# After tests fail, implement sequentially:
Task: "Implement Chunk class in src/world/chunk.py"                  # T010
Task: "Implement World class in src/world/world.py"                  # T011 (depends on T010)
Task: "Implement Player controller in src/player/player.py"          # T012 (parallel with T010-T011)
Task: "Create main entry point in src/main.py"                       # T013 (depends on T011, T012)
```

## Parallel Example: User Story 2

```bash
# Launch all US2 test-writing tasks together:
Task: "Write unit tests for Inventory in tests/unit/test_inventory.py"     # T014
Task: "Write unit tests for RecipeRegistry in tests/unit/test_crafting.py" # T015

# Parallel implementation tasks:
Task: "Implement ItemDrop entity in src/entities/item_drop.py"       # T017
Task: "Implement RecipeRegistry in src/crafting/recipe.py"           # T018
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Launch game with `python src/main.py`, verify navigation and block interaction
5. Demo/share if ready

### Incremental Delivery

1. Setup + Foundational → project skeleton ready
2. Add US1 → playable voxel world (MVP!)
3. Add US2 → resource collection and crafting (progression layer)
4. Add US3 → survival tension (day/night + enemies)
5. Add US4 → creative building (long-term engagement)
6. Add US5 → persistent saves (player investment)
7. Polish → production-ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Phase 1 + Phase 2 together
2. Once Foundational (Phase 2) is done:
   - Developer A: User Story 1 (world + player)
   - Developer B: User Story 2 (inventory + crafting)
   - Developer C: User Story 5 (save/load infrastructure)
3. Stories complete → integrate → continue with US3, US4, Polish

---

## Summary

| Phase | Story | Tasks | Parallel Tasks |
|-------|-------|-------|----------------|
| Phase 1: Setup | — | T001–T004 | T003, T004 |
| Phase 2: Foundational | — | T005–T007 | T006, T007 |
| Phase 3: US1 (P1) | Voxel World | T008–T013 | T008, T009, T012 |
| Phase 4: US2 (P2) | Resources & Crafting | T014–T021 | T014, T015, T017, T018 |
| Phase 5: US3 (P3) | Day/Night & Enemies | T022–T028 | T022, T023 |
| Phase 6: US4 (P4) | Build Structures | T029–T033 | T029, T033 |
| Phase 7: US5 (P5) | Save & Load | T034–T039 | T034, T035 |
| Polish | — | T040–T044 | T040, T041, T043 |
| **Total** | | **44 tasks** | **19 parallel** |

---

## Notes

- [P] tasks = different files or non-overlapping concerns; safe to run in parallel
- [Story] label maps each task to a specific user story for traceability
- Each user story is independently completable and testable
- TDD: always verify tests **FAIL** before writing implementation
- Commit after each task or logical group
- Stop at each **Checkpoint** to validate the story works independently
- Avoid: vague tasks, same-file conflicts within a story, cross-story dependencies that break independence
