"""Unit tests for RecipeRegistry and craft function (User Story 2)."""
import pytest
from src.player.inventory import Inventory, ItemType
from src.crafting.recipe import RecipeRegistry, Recipe, craft, build_default_registry


class TestRecipeRegistry:
    def _simple_registry(self) -> RecipeRegistry:
        reg = RecipeRegistry()
        reg.register(
            [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]],
            ItemType.WOOD_PLANKS,
            4,
        )
        return reg

    def test_find_recipe_returns_matching_recipe(self):
        reg = self._simple_registry()
        grid = [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]]
        recipe = reg.find_recipe(grid)
        assert recipe is not None
        assert recipe.result == ItemType.WOOD_PLANKS
        assert recipe.result_count == 4

    def test_find_recipe_returns_none_for_unknown_pattern(self):
        reg = self._simple_registry()
        grid = [[ItemType.STONE, None, None], [None, None, None], [None, None, None]]
        assert reg.find_recipe(grid) is None

    def test_get_all_recipes_returns_list(self):
        reg = self._simple_registry()
        recipes = reg.get_all_recipes()
        assert len(recipes) == 1
        assert isinstance(recipes[0], Recipe)

    def test_default_registry_has_at_least_ten_recipes(self):
        reg = build_default_registry()
        assert len(reg.get_all_recipes()) >= 10


class TestCraft:
    def test_craft_valid_recipe_returns_item(self):
        reg = RecipeRegistry()
        reg.register(
            [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]],
            ItemType.WOOD_PLANKS,
            4,
        )
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 1)
        grid = [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]]
        result = craft(reg, grid, inv)
        assert result == ItemType.WOOD_PLANKS
        assert inv.has_items(ItemType.WOOD_PLANKS, 4)
        assert not inv.has_items(ItemType.WOOD, 1)

    def test_craft_insufficient_materials_returns_none(self):
        reg = RecipeRegistry()
        reg.register(
            [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]],
            ItemType.WOOD_PLANKS,
            4,
        )
        inv = Inventory()  # empty
        grid = [[ItemType.WOOD, None, None], [None, None, None], [None, None, None]]
        result = craft(reg, grid, inv)
        assert result is None

    def test_craft_unknown_recipe_returns_none(self):
        reg = build_default_registry()
        inv = Inventory()
        inv.add_item(ItemType.TORCH, 5)
        # Random nonsense grid
        grid = [[ItemType.TORCH, ItemType.TORCH, None], [None, None, None], [None, None, None]]
        result = craft(reg, grid, inv)
        assert result is None
