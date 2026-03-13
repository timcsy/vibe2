"""Main menu — pure-logic state (Ursina rendering in main.py)."""
from __future__ import annotations

from enum import Enum, auto
from typing import List


class MenuAction(Enum):
    NONE = auto()
    NEW_GAME = auto()
    LOAD_GAME = auto()
    QUIT = auto()


class MainMenu:
    """Tracks main menu state: available saves, selected action."""

    def __init__(self, available_saves: List[str] = None) -> None:
        self.available_saves: List[str] = available_saves or []
        self.is_open: bool = True
        self.pending_action: MenuAction = MenuAction.NONE
        self.selected_save: str = ""

    def new_game(self) -> None:
        self.pending_action = MenuAction.NEW_GAME
        self.is_open = False

    def load_game(self, save_name: str) -> None:
        self.selected_save = save_name
        self.pending_action = MenuAction.LOAD_GAME
        self.is_open = False

    def quit(self) -> None:
        self.pending_action = MenuAction.QUIT

    def reset(self) -> None:
        self.pending_action = MenuAction.NONE
        self.is_open = True
