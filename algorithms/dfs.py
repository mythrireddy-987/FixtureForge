import time

def dfs(graph, current, goal, visited, path):
    visited.add(current)
    path.append(current)

    if current == goal:
        return path.copy()

    for neighbour in graph[current]:
        if neighbour not in visited:
            result = dfs(graph, neighbour, goal, visited, path)

            if result:
                return result

    path.pop()
    return None


if __name__ == "__main__":
    graph = {
        "Stadium A": ["Stadium B", "Stadium C"],
        "Stadium B": ["Stadium A", "Stadium D"],
        "Stadium C": ["Stadium A", "Stadium D"],
        "Stadium D": ["Stadium B", "Stadium C"]
    }

    print("DFS SEARCH")

    visited = set()
    start_time = time.perf_counter()

    path = dfs(graph, "Stadium A", "Stadium D", visited, [])

    end_time = time.perf_counter()

    print("DFS Route:", path)
    print("DFS Nodes Expanded:", len(visited))
    print("DFS Execution Time:", end_time - start_time, "seconds")