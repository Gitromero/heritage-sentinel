from restoration_graph import START, GOAL, available_actions, apply_action
from tester import BEGIN, ACE

from planner import bfs_search

if __name__ == "__main__":
    plan = bfs_search(START, GOAL, available_actions, apply_action)
    plan1 = bfs_search(BEGIN, ACE, available_actions, apply_action)
    print("Restoration plan:", plan)
    print("Restoration plan:", plan1)

