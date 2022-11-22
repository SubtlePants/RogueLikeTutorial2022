from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction, WaitAction

if TYPE_CHECKING:
    from engine import Engine

MOVE_DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
    "RightUp": (1, -1),
    "LeftUp": (-1, -1),
    "RightDown": (1, 1),
    "LeftDown": (-1, 1),
    "Wait": (0, 0)
}

MOVE_KEYS = {
    # Arrow keys
    tcod.event.K_UP: MOVE_DIRECTIONS["Up"],
    tcod.event.K_DOWN: MOVE_DIRECTIONS["Down"],
    tcod.event.K_LEFT: MOVE_DIRECTIONS["Left"],
    tcod.event.K_RIGHT: MOVE_DIRECTIONS["Right"],
    tcod.event.K_HOME: MOVE_DIRECTIONS["LeftUp"],
    tcod.event.K_END: MOVE_DIRECTIONS["LeftDown"],
    tcod.event.K_PAGEUP: MOVE_DIRECTIONS["RightUp"],
    tcod.event.K_PAGEDOWN: MOVE_DIRECTIONS["RightDown"],
    # Numpad keys
    tcod.event.K_KP_1: MOVE_DIRECTIONS["LeftDown"],
    tcod.event.K_KP_2: MOVE_DIRECTIONS["Down"],
    tcod.event.K_KP_3: MOVE_DIRECTIONS["RightDown"],
    tcod.event.K_KP_4: MOVE_DIRECTIONS["Left"],
    tcod.event.K_KP_6: MOVE_DIRECTIONS["Right"],
    tcod.event.K_KP_7: MOVE_DIRECTIONS["LeftUp"],
    tcod.event.K_KP_8: MOVE_DIRECTIONS["Up"],
    tcod.event.K_KP_9: MOVE_DIRECTIONS["RightUp"],
    # Vi keys
    tcod.event.K_h: MOVE_DIRECTIONS["Left"],
    tcod.event.K_j: MOVE_DIRECTIONS["Down"],
    tcod.event.K_k: MOVE_DIRECTIONS["Up"],
    tcod.event.K_l: MOVE_DIRECTIONS["Right"],
    tcod.event.K_y: MOVE_DIRECTIONS["LeftUp"],
    tcod.event.K_u: MOVE_DIRECTIONS["RightUp"],
    tcod.event.K_b: MOVE_DIRECTIONS["LeftDown"],
    tcod.event.K_n: MOVE_DIRECTIONS["RightDown"],
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)

        # No Valid Key Was Pressed
        return action
