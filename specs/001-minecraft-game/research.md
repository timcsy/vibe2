# Research: Minecraft-Like Sandbox Game

**Feature**: 001-minecraft-game  
**Phase**: 0 - Research  
**Date**: 2026-03-13

## Research Questions & Decisions

### 1. Game Engine Selection

**Decision**: Ursina Engine (Python, built on Panda3D)  
**Rationale**: 
- Python-native: matches team skill set, rapid prototyping
- Built-in 3D rendering, collision, input handling
- Active community with voxel game examples
- Simpler API than raw Panda3D or Unity/Godot
- Open source (MIT license)
- Alternatives considered: Pygame (2D only, no 3D), Godot (separate scripting language, heavier), Unity (C#, commercial, heavier toolchain), raw OpenGL (too low-level for this scope)

### 2. Procedural World Generation

**Decision**: Perlin/Simplex noise via the `noise` library  
**Rationale**:
- Industry standard for voxel terrain generation
- Produces natural-looking hills, valleys, and caves
- Fast enough for real-time chunk generation
- `noise` package (Python) is lightweight and well-tested
- Alternatives considered: random heightmap (too jagged), fractal noise (more complex, marginal improvement)

### 3. Chunk System

**Decision**: 16×16×16 block chunks  
**Rationale**:
- Standard Minecraft-inspired chunk size
- Balances memory usage vs. draw call overhead
- Enables lazy loading: only render nearby chunks
- Simplifies spatial indexing (integer chunk coordinates)
- Alternatives considered: 32×32×32 (too many blocks per chunk for Python), flat 2D chunks (no underground support)

### 4. Save Format

**Decision**: JSON for world metadata + binary pickle for block data  
**Rationale**:
- JSON: human-readable metadata (player pos, health, inventory) — easy to debug
- Pickle: compact binary format for bulk block data — faster I/O than JSON for large arrays
- Alternatives considered: SQLite (overkill for single-player), pure JSON (too slow for large worlds), HDF5 (heavy dependency)

### 5. Crafting System

**Decision**: Grid-based recipe dictionary (pattern → output)  
**Rationale**:
- Matches Minecraft's familiar 3×3 grid crafting
- Simple to define recipes as pattern strings
- Easy to extend with new recipes
- Alternatives considered: free-form crafting (less discoverable), tree-based crafting (different UX paradigm)

### 6. Enemy AI

**Decision**: Simple state machine (Idle → Detect → Chase → Attack)  
**Rationale**:
- Sufficient for basic survival gameplay
- Easy to implement and test
- Performance-friendly for Python
- Alternatives considered: behavior trees (overkill), NavMesh pathfinding (complex, not needed for open voxel terrain)

### 7. Testing Strategy

**Decision**: pytest with unit tests for pure logic; integration tests for gameplay flows  
**Rationale**:
- pytest is the Python testing standard
- Game engine (Ursina) code is hard to unit-test in isolation → abstract game logic from rendering
- Pure Python modules (inventory, crafting, save, health) are fully unit-testable without engine
- Alternatives considered: unittest (more verbose), hypothesis (property-based, useful for world gen but secondary)

## Technology Summary

| Concern | Technology | Version |
|---------|-----------|---------|
| Language | Python | 3.11 |
| Game Engine | Ursina | 6.x |
| Underlying 3D | Panda3D | (via Ursina) |
| Noise Generation | noise | 1.2.x |
| Testing | pytest | 7.x |
| Serialization | json + pickle | stdlib |
| Package Management | pip + requirements.txt | — |
