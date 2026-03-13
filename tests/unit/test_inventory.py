"""Unit tests for Inventory class (User Story 2)."""
import pytest
from src.player.inventory import Inventory, ItemStack, ItemType


class TestInventory:
    def test_add_item_returns_true_when_space(self):
        inv = Inventory()
        assert inv.add_item(ItemType.WOOD, 5) is True

    def test_add_item_increases_quantity(self):
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 3)
        assert inv.has_items(ItemType.WOOD, 3)

    def test_add_item_stacks_with_existing(self):
        inv = Inventory()
        inv.add_item(ItemType.STONE, 30)
        inv.add_item(ItemType.STONE, 30)
        assert inv.has_items(ItemType.STONE, 60)

    def test_add_item_returns_false_when_full(self):
        inv = Inventory(max_slots=1)
        # Fill the only slot with a single-stack item
        inv.add_item(ItemType.WOOD_PICKAXE, 1)
        result = inv.add_item(ItemType.STONE_PICKAXE, 1)
        assert result is False

    def test_remove_item_returns_true_when_sufficient(self):
        inv = Inventory()
        inv.add_item(ItemType.COAL, 10)
        assert inv.remove_item(ItemType.COAL, 5) is True

    def test_remove_item_decreases_quantity(self):
        inv = Inventory()
        inv.add_item(ItemType.COAL, 10)
        inv.remove_item(ItemType.COAL, 4)
        assert inv.has_items(ItemType.COAL, 6)
        assert not inv.has_items(ItemType.COAL, 7)

    def test_remove_item_returns_false_when_insufficient(self):
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 3)
        assert inv.remove_item(ItemType.WOOD, 10) is False

    def test_remove_item_clears_slot_when_zero(self):
        inv = Inventory()
        inv.add_item(ItemType.STICK, 1)
        inv.remove_item(ItemType.STICK, 1)
        assert not inv.has_items(ItemType.STICK, 1)

    def test_has_items_true_when_enough(self):
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 10)
        assert inv.has_items(ItemType.WOOD, 10) is True

    def test_has_items_false_when_insufficient(self):
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 5)
        assert inv.has_items(ItemType.WOOD, 6) is False

    def test_get_hotbar_returns_first_nine_slots(self):
        inv = Inventory()
        hotbar = inv.get_hotbar()
        assert len(hotbar) == 9

    def test_get_selected_item_returns_correct_slot(self):
        inv = Inventory()
        inv.add_item(ItemType.TORCH, 4)
        inv.selected_slot = 0
        item = inv.get_selected_item()
        assert item is not None
        assert item.item_type == ItemType.TORCH

    def test_to_dict_round_trip(self):
        inv = Inventory()
        inv.add_item(ItemType.WOOD, 5)
        inv.add_item(ItemType.STONE, 3)
        data = inv.to_dict()
        inv2 = Inventory()
        inv2.from_dict(data)
        assert inv2.has_items(ItemType.WOOD, 5)
        assert inv2.has_items(ItemType.STONE, 3)

    def test_full_inventory_rejection(self):
        inv = Inventory(max_slots=2)
        inv.add_item(ItemType.WOOD_PICKAXE, 1)
        inv.add_item(ItemType.STONE_PICKAXE, 1)
        result = inv.add_item(ItemType.IRON_PICKAXE, 1)
        assert result is False
