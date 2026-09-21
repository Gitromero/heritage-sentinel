# planner.py — search algorithm only. No mention of statues, cracks, or pigment allowed here.
from collections import deque

def bfs_search(start, goal, available_actions, apply_action):
    frontier = deque([(start, [])])
    visited = {start}
    while frontier:
        state, path = frontier.popleft()
        if state == goal:
            return path
        # TODO: for each action available from `state`, compute the next
        # state, and if it hasn't been visited, add it to the frontier
        # with the updated path.
        ...
    return None  # no valid sequence exists