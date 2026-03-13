"""CraftingUI — pure-logic crafting interface (Ursina rendering in main.py)."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from src.player.inventory import ItemType
from src.crafting.recipe import RecipeRegistry, Recipe

if TYPE_CHECKING:
    from src.player.inventory import Inventory

GRID_SIZE = 3


class CraftingUI:
    """3×3 crafting grid state. Ursina widgets wired in main.py."""

    def __init__(self, registry: RecipeRegistry) -> None:
        self.registry: RecipeRegistry = registry
        self.grid: List[List[Optional[ItemType]]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.is_open: bool = False
        self._preview: Optional[Recipe] = None

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False
        self.clear_grid()

    def toggle(self) -> None:
        if self.is_open:
            self.close()
        else:
            self.open()

    def set_slot(self, row: int, col: int, item_type: Optional[ItemType]) -> None:
        self.grid[row][col] = item_type
        self._preview = self.registry.find_recipe(self.grid)

    def clear_grid(self) -> None:
        self.grid = [[None, None, None] for _ in range(GRID_SIZE)]
        self._preview = None

    def get_preview(self) -> Optional[Recipe]:
        return self._preview

    def craft(self, inventory: "Inventory") -> Optional[ItemType]:
        """Attempt to craft using the current grid. Returns crafted item or None."""
        from src.crafting.recipe import craft as do_craft
        result = do_craft(self.registry, self.grid, inventory)
        if result is not None:
            self.clear_grid()
        return result
