# tests/test_planner.py
import time

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


def make_problem(actions):
    """Build available_actions/apply_action for an arbitrary ACTIONS dict,
    mirroring restoration_graph.py (whose functions are bound to its own ACTIONS)."""
    def available(state):
        return [a for a, info in actions.items()
                if a not in state and info["requires"].issubset(state)]

    def apply(state, action):
        return state | {action}

    return available, apply


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
    # Case 1: goal names an action that doesn't exist in ACTIONS.
    impossible_goal = GOAL | {"gild_statue"}
    assert bfs_search(START, impossible_goal, available_actions, apply_action) is None

    # Case 2: circular prerequisites -- a needs b, b needs a. Neither can ever run.
    circular = {
        "a": {"requires": {"b"}, "cost": 1},
        "b": {"requires": {"a"}, "cost": 1},
        "c": {"requires": set(), "cost": 1},
    }
    available, apply = make_problem(circular)
    assert bfs_search(frozenset(), frozenset(circular), available, apply) is None

    # Case 3: prerequisite on an action that doesn't exist.
    dangling = {"a": {"requires": {"ghost"}, "cost": 1}}
    available, apply = make_problem(dangling)
    assert bfs_search(frozenset(), frozenset(dangling), available, apply) is None


def test_large_action_set_terminates():
    # 20 actions in a single chain: step_i requires step_{i-1}.
    n = 20
    big = {f"step_{i}": {"requires": {f"step_{i - 1}"} if i else set(), "cost": 1}
           for i in range(n)}
    available, apply = make_problem(big)

    t0 = time.perf_counter()
    plan = bfs_search(frozenset(), frozenset(big), available, apply)
    elapsed = time.perf_counter() - t0

    assert plan is not None
    assert is_valid_plan(plan, big)
    assert elapsed < 2.0

    # Same chain with an unreachable goal must also terminate (exhaust and return None).
    t0 = time.perf_counter()
    assert bfs_search(frozenset(), frozenset(big) | {"ghost"}, available, apply) is None
    assert time.perf_counter() - t0 < 2.0
