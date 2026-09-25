# restoration_graph.py — problem definition only.
# planner.py must not know anything specific to this file.

ACTIONS = {
    "Practive_Exam": {"requires": set(), "cost": 3},
    "Google": {"requires": {"Syllabus"}, "cost": 2},
    "Syllabus": {"requires": set(), "cost": 1},
    "Study": {"requires": {"Google"}, "cost": 2},
}

ACE = frozenset(ACTIONS.keys())
BEGIN = frozenset()

def available_actions(state):
    """Actions whose prerequisites are satisfied and not already done."""
    return [a for a, info in ACTIONS.items()
            if a not in state and info["requires"].issubset(state)]

def apply_action(state, action):
    return state | {action}