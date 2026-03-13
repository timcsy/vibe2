"""Recipe registry and craft function for Minecraft-like crafting system."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, TYPE_CHECKING

from src.player.inventory import ItemType, Inventory

if TYPE_CHECKING:
    pass


@dataclass
class Recipe:
    pattern: List[List[Optional[ItemType]]]
    result: ItemType
    result_count: int = 1

    def _ingredients(self) -> dict[ItemType, int]:
        counts: dict[ItemType, int] = {}
        for row in self.pattern:
            for item in row:
                if item is not None:
                    counts[item] = counts.get(item, 0) + 1
        return counts


class RecipeRegistry:
    def __init__(self) -> None:
        self._recipes: List[Recipe] = []

    def register(
        self,
        pattern: List[List[Optional[ItemType]]],
        result: ItemType,
        count: int = 1,
    ) -> None:
        self._recipes.append(Recipe(pattern=pattern, result=result, result_count=count))

    def find_recipe(
        self, grid: List[List[Optional[ItemType]]]
    ) -> Optional[Recipe]:
        """Return the first recipe matching the grid, or None."""
        grid_flat = tuple(item for row in grid for item in row)
        for recipe in self._recipes:
            recipe_flat = tuple(item for row in recipe.pattern for item in row)
            if recipe_flat == grid_flat:
                return recipe
        return None

    def get_all_recipes(self) -> List[Recipe]:
        return list(self._recipes)


def craft(
    registry: RecipeRegistry,
    grid: List[List[Optional[ItemType]]],
    inventory: Inventory,
) -> Optional[ItemType]:
    """
    Attempt to craft using the given grid and inventory.
    Returns the crafted ItemType if successful, None otherwise.
    """
    recipe = registry.find_recipe(grid)
    if recipe is None:
        return None
    ingredients = recipe._ingredients()
    # Check inventory has all required materials
    for item_type, qty in ingredients.items():
        if not inventory.has_items(item_type, qty):
            return None
    # Consume ingredients
    for item_type, qty in ingredients.items():
        inventory.remove_item(item_type, qty)
    # Add result
    inventory.add_item(recipe.result, recipe.result_count)
    return recipe.result


def build_default_registry() -> RecipeRegistry:
    """Build a registry with the default set of game recipes (≥10)."""
    r = RecipeRegistry()
    W = ItemType.WOOD
    P = ItemType.WOOD_PLANKS
    S = ItemType.STICK
    St = ItemType.STONE
    C = ItemType.COAL
    Fe = ItemType.IRON_INGOT
    N = None

    # Wood planks (4): 1 Wood → 4 planks
    r.register([[W, N, N], [N, N, N], [N, N, N]], ItemType.WOOD_PLANKS, 4)

    # Sticks (4): 2 planks stacked → 4 sticks
    r.register([[P, N, N], [P, N, N], [N, N, N]], ItemType.STICK, 4)

    # Crafting table: 4 planks in 2×2
    r.register([[P, P, N], [P, P, N], [N, N, N]], ItemType.CRAFTING_TABLE, 1)

    # Torch (4): coal on top of stick
    r.register([[C, N, N], [S, N, N], [N, N, N]], ItemType.TORCH, 4)

    # Wood pickaxe: 3 planks in row + 2 sticks
    r.register([[P, P, P], [N, S, N], [N, S, N]], ItemType.WOOD_PICKAXE, 1)

    # Stone pickaxe: 3 stone in row + 2 sticks
    r.register([[St, St, St], [N, S, N], [N, S, N]], ItemType.STONE_PICKAXE, 1)

    # Iron pickaxe: 3 iron in row + 2 sticks
    r.register([[Fe, Fe, Fe], [N, S, N], [N, S, N]], ItemType.IRON_PICKAXE, 1)

    # Wood sword: 2 planks + 1 stick
    r.register([[N, P, N], [N, P, N], [N, S, N]], ItemType.WOOD_SWORD, 1)

    # Stone sword: 2 stone + 1 stick
    r.register([[N, St, N], [N, St, N], [N, S, N]], ItemType.STONE_SWORD, 1)

    # Iron sword: 2 iron + 1 stick
    r.register([[N, Fe, N], [N, Fe, N], [N, S, N]], ItemType.IRON_SWORD, 1)

    # Iron ingot from iron ore (smelting proxy): 1 iron ore + 1 coal → 1 iron ingot
    r.register([[ItemType.IRON_ORE, C, N], [N, N, N], [N, N, N]], ItemType.IRON_INGOT, 1)

    return r
