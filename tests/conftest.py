# Make modules in src/ importable as top-level (e.g. `from planner import bfs_search`).
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
