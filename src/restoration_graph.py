# restoration_graph.py — problem definition only.
# planner.py must not know anything specific to this file.

ACTIONS = {
    "stabilize_base": {"requires": set(), "cost": 3},
    "seal_crack": {"requires": {"stabilize_base"}, "cost": 2},
    "clean_surface": {"requires": set(), "cost": 1},
    "restore_pigment": {"requires": {"clean_surface"}, "cost": 2},
}

GOAL = frozenset(ACTIONS.keys())
START = frozenset()

def available_actions(state):
    """Actions whose prerequisites are satisfied and not already done."""
    return [a for a, info in ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def apply_action(state, action):
    return state | {action}