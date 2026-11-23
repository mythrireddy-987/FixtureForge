import time

from bfs import bfs
from dfs import dfs
from route_planner import (
    weighted_graph,
    simple_graph,
    heuristic,
    heuristic2,
    uniform_cost_search,
    greedy_best_first_search,
    a_star_search
)


def calculate_path_cost(path):
    total_cost = 0

    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        for neighbour, distance in weighted_graph[current]:
            if neighbour == next_node:
                total_cost += distance
                break
        else:
            for neighbour, distance in weighted_graph[next_node]:
                if neighbour == current:
                    total_cost += distance
                    break

    return total_cost


start = "Stadium A"
goal = "Stadium D"

results = []


# BFS
start_time = time.perf_counter()
path, nodes = bfs(simple_graph, start, goal)
elapsed = time.perf_counter() - start_time
results.append(("BFS", path, calculate_path_cost(path), nodes, elapsed))


# DFS
start_time = time.perf_counter()
visited = set()
path = dfs(simple_graph, start, goal, visited, [])
elapsed = time.perf_counter() - start_time
nodes = len(visited)
results.append(("DFS", path, calculate_path_cost(path), nodes, elapsed))


# UCS
start_time = time.perf_counter()
path, cost, nodes = uniform_cost_search(weighted_graph, start, goal)
elapsed = time.perf_counter() - start_time
results.append(("UCS", path, cost, nodes, elapsed))


# Greedy Best-First Search
start_time = time.perf_counter()
path, cost, nodes = greedy_best_first_search(
    simple_graph, heuristic, start, goal
)
elapsed = time.perf_counter() - start_time
results.append(("Greedy", path, cost, nodes, elapsed))


# A* with Heuristic 1
start_time = time.perf_counter()
path, cost, nodes = a_star_search(
    weighted_graph, heuristic, start, goal
)
elapsed = time.perf_counter() - start_time
results.append(("A* Heuristic 1", path, cost, nodes, elapsed))


# A* with Heuristic 2
start_time = time.perf_counter()
path, cost, nodes = a_star_search(
    weighted_graph, heuristic2, start, goal
)
elapsed = time.perf_counter() - start_time
results.append(("A* Heuristic 2", path, cost, nodes, elapsed))


# Display comparison table
print("\nSEARCH ALGORITHM COMPARISON")
print("-" * 100)
print(f"{'Algorithm':<20}{'Route':<30}{'Path Cost':<15}{'Nodes':<15}{'Time (seconds)'}")
print("-" * 100)

for name, path, cost, nodes, elapsed in results:
    route = " -> ".join(path) if path else "No route"
    print(f"{name:<20}{route:<30}{cost:<15}{nodes:<15}{elapsed:.8f}")

print("-" * 100)