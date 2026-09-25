# tests/test_planner.py
import time

import restoration_graph
from restoration_graph import ACTIONS, START, GOAL, available_actions, apply_action
from planner import bfs_search


def is_valid_plan(plan, actions=ACTIONS):
    """A plan is valid if every action's prerequisites are satisfied by
    the actions before it, and every required action appears exactly once."""
    completed = set()
    for action in plan:
        if action in completed:
            return False          # duplicate action
        if not actions[action]["requires"].issubset(completed):
            return False          # prerequisite violated
        completed.add(action)
    return completed == set(actions.keys())


def test_finds_a_valid_plan():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert plan is not None
    assert is_valid_plan(plan)


def test_trivial_already_done():
    # start == goal: the plan should be empty, not None, not a crash
    plan = bfs_search(GOAL, GOAL, available_actions, apply_action)
    assert plan == []


def test_plan_has_no_duplicate_actions():
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    assert len(plan) == len(set(plan))
def test_no_solution_returns_none():
    # Add an action to the goal that can never be completed.
    impossible_goal = GOAL | {"impossible_action"}

    plan = bfs_search(START, impossible_goal, available_actions, apply_action)

    # BFS should exhaust all reachable states and return None.
    assert plan is None


def test_large_action_set_terminates():
    # Create 15 actions in a chain, where each step requires the previous step.
    big_actions = {
        f"step_{i}": {
            "requires": {f"step_{i - 1}"} if i > 0 else set(),
            "cost": 1
        }
        for i in range(15)
    }

    # Same behavior as restoration_graph.available_actions,
    # but using our larger test action set.
    def big_available_actions(state):
        return [
            action for action, info in big_actions.items()
            if action not in state
            and info["requires"].issubset(state)
        ]

    def big_apply_action(state, action):
        return state | {action}

    start = frozenset()
    goal = frozenset(big_actions)

    # Time the search to make sure the larger problem terminates quickly.
    t0 = time.perf_counter()

    plan = bfs_search(
        start,
        goal,
        big_available_actions,
        big_apply_action
    )

    elapsed = time.perf_counter() - t0

    # Make sure BFS found a valid plan and finished within the time limit.
    assert plan is not None
    assert is_valid_plan(plan, big_actions)
    assert elapsed < 2.0