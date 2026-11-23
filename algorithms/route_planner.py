import heapq
import time


# WEIGHTED STADIUM NETWORK

weighted_graph = {
    "Stadium A": [("Stadium B", 10), ("Stadium C", 5)],
    "Stadium B": [("Stadium D", 8)],
    "Stadium C": [("Stadium D", 3)],
    "Stadium D": []
}


# SIMPLE STADIUM NETWORK

simple_graph = {
    "Stadium A": ["Stadium B", "Stadium C"],
    "Stadium B": ["Stadium D"],
    "Stadium C": ["Stadium D"],
    "Stadium D": []
}


# HEURISTIC VALUES

heuristic = {
    "Stadium A": 8,
    "Stadium B": 7,
    "Stadium C": 3,
    "Stadium D": 0
}

heuristic2 = {
    "Stadium A": 6,
    "Stadium B": 5,
    "Stadium C": 2,
    "Stadium D": 0
}


# CALCULATE TOTAL ROUTE COST

def calculate_path_cost(graph, path):
    total_cost = 0

    for index in range(len(path) - 1):
        current = path[index]
        next_stadium = path[index + 1]

        for neighbour, distance in graph.get(current, []):
            if neighbour == next_stadium:
                total_cost += distance
                break

    return total_cost


# UNIFORM COST SEARCH

def uniform_cost_search(graph, start, goal):
    priority_queue = [(0, start, [start])]
    best_cost = {start: 0}
    nodes_expanded = 0

    while priority_queue:
        current_cost, current, path = heapq.heappop(priority_queue)

        if current_cost > best_cost.get(current, float("inf")):
            continue

        nodes_expanded += 1

        if current == goal:
            return path, current_cost, nodes_expanded

        for neighbour, distance in graph.get(current, []):
            new_cost = current_cost + distance

            if new_cost < best_cost.get(neighbour, float("inf")):
                best_cost[neighbour] = new_cost

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbour, path + [neighbour])
                )

    return None, float("inf"), nodes_expanded


# GREEDY BEST FIRST SEARCH

def greedy_best_first_search(graph, heuristic, start, goal):
    priority_queue = [(heuristic[start], start, [start])]
    visited = set()
    nodes_expanded = 0

    while priority_queue:
        h_value, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            route_cost = calculate_path_cost(weighted_graph, path)
            return path, route_cost, nodes_expanded

        for neighbour in graph.get(current, []):
            if neighbour not in visited:
                heapq.heappush(
                    priority_queue,
                    (heuristic[neighbour], neighbour, path + [neighbour])
                )

    return None, float("inf"), nodes_expanded


# A STAR SEARCH

def a_star_search(graph, heuristic, start, goal):
    priority_queue = [(heuristic[start], 0, start, [start])]
    best_cost = {start: 0}
    nodes_expanded = 0

    while priority_queue:
        estimated_total, current_cost, current, path = heapq.heappop(
            priority_queue
        )

        if current_cost > best_cost.get(current, float("inf")):
            continue

        nodes_expanded += 1

        if current == goal:
            return path, current_cost, nodes_expanded

        for neighbour, distance in graph.get(current, []):
            new_cost = current_cost + distance

            if new_cost < best_cost.get(neighbour, float("inf")):
                best_cost[neighbour] = new_cost
                new_estimate = new_cost + heuristic[neighbour]

                heapq.heappush(
                    priority_queue,
                    (
                        new_estimate,
                        new_cost,
                        neighbour,
                        path + [neighbour]
                    )
                )

    return None, float("inf"), nodes_expanded


# TESTING THE SEARCH ALGORITHMS

if __name__ == "__main__":

    print("UNIFORM COST SEARCH")

    start_time = time.perf_counter()

    path, cost, nodes = uniform_cost_search(
        weighted_graph, "Stadium A", "Stadium D"
    )

    end_time = time.perf_counter()

    print("UCS Route:", path)
    print("UCS Travel Cost:", cost)
    print("UCS Nodes Expanded:", nodes)
    print("UCS Execution Time:", end_time - start_time, "seconds")


    print("\nGREEDY BEST FIRST SEARCH")

    start_time = time.perf_counter()

    path, cost, nodes = greedy_best_first_search(
        simple_graph, heuristic, "Stadium A", "Stadium D"
    )

    end_time = time.perf_counter()

    print("Greedy Route:", path)
    print("Greedy Travel Cost:", cost)
    print("Greedy Nodes Expanded:", nodes)
    print("Greedy Execution Time:", end_time - start_time, "seconds")


    print("\nA STAR SEARCH")

    start_time = time.perf_counter()

    path, cost, nodes = a_star_search(
        weighted_graph, heuristic, "Stadium A", "Stadium D"
    )

    end_time = time.perf_counter()

    print("A* Route:", path)
    print("A* Travel Cost:", cost)
    print("A* Nodes Expanded:", nodes)
    print("A* Execution Time:", end_time - start_time, "seconds")