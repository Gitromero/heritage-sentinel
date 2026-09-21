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
