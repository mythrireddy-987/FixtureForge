import sys
import os
import time

from flask import Blueprint, request, jsonify

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALGORITHMS_PATH = os.path.join(PROJECT_ROOT, "algorithms")

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, ALGORITHMS_PATH)

from bfs import bfs
from dfs import dfs

from route_planner import (
    weighted_graph,
    simple_graph,
    heuristic,
    uniform_cost_search,
    greedy_best_first_search,
    a_star_search
)

route_api = Blueprint("route_api", __name__)


@route_api.route("/find-route", methods=["POST"])
def find_route():

    data = request.get_json()

    start = data.get("start")
    goal = data.get("goal")
    algorithm = data.get("algorithm", "all")

    if not start or not goal:
        return jsonify({
            "error": "Select both starting and destination stadiums."
        }), 400

    if start not in weighted_graph or goal not in weighted_graph:
        return jsonify({
            "error": "Invalid stadium selection."
        }), 400

    algorithms = {
        "BFS": lambda: bfs(simple_graph, start, goal),
        "DFS": lambda: dfs(simple_graph, start, goal, set(), []),
        "UCS": lambda: uniform_cost_search(weighted_graph, start, goal),
        "Greedy": lambda: greedy_best_first_search(
            simple_graph, heuristic, start, goal
        ),
        "A*": lambda: a_star_search(
            weighted_graph, heuristic, start, goal
        )
    }

    if algorithm == "all":
        selected_algorithms = algorithms
    elif algorithm in algorithms:
        selected_algorithms = {algorithm: algorithms[algorithm]}
    else:
        return jsonify({"error": "Invalid search algorithm."}), 400

    results = []

    for name, search_function in selected_algorithms.items():

        start_time = time.perf_counter()
        result = search_function()
        elapsed_time = time.perf_counter() - start_time

        if name == "BFS":
            path, nodes = result
            cost = 0

            if path:
                for i in range(len(path) - 1):
                    for neighbour, distance in weighted_graph[path[i]]:
                        if neighbour == path[i + 1]:
                            cost += distance
                            break

        elif name == "DFS":
            path = result
            nodes = len(set(path)) if path else 0
            cost = 0

            if path:
                for i in range(len(path) - 1):
                    for neighbour, distance in weighted_graph[path[i]]:
                        if neighbour == path[i + 1]:
                            cost += distance
                            break

        else:
            path, cost, nodes = result

        results.append({
            "algorithm": name,
            "route": path,
            "travel_cost": cost if path else None,
            "nodes_expanded": nodes,
            "execution_time": elapsed_time
        })

    return jsonify({"results": results})