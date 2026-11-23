from collections import deque
import time


def bfs(graph, start, goal):

    visited = set()
    queue = deque([(start, [start])])

    visited.add(start)
    nodes_expanded = 0

    while queue:

        current, path = queue.popleft()

        if current == goal:
            return path, nodes_expanded

        nodes_expanded += 1

        for neighbour in graph[current]:

            if neighbour not in visited:

                visited.add(neighbour)
                queue.append((neighbour, path + [neighbour]))

    return None, nodes_expanded


if __name__ == "__main__":
    # Sample sports travel network
    graph = {
        "Stadium A": ["Stadium B", "Stadium C"],
        "Stadium B": ["Stadium A", "Stadium D"],
        "Stadium C": ["Stadium A", "Stadium D"],
        "Stadium D": ["Stadium B", "Stadium C"]
    }

    print("BFS SEARCH")
    start_time = time.perf_counter()
    path, nodes = bfs(graph, "Stadium A", "Stadium D")
    end_time = time.perf_counter()

    print("BFS Route:", path)
    print("BFS Nodes Expanded:", nodes)
    print("BFS Execution Time:", end_time - start_time, "seconds")