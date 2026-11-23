import matplotlib.pyplot as plt

# Two heuristics from route_planner.py
stadiums = ["Stadium A", "Stadium B", "Stadium C", "Stadium D"]

heuristic1 = [7, 6, 2, 0]
heuristic2 = [5, 4, 1, 0]

# Create comparison chart
positions = range(len(stadiums))

plt.plot(positions, heuristic1, marker="o", label="Heuristic 1")
plt.plot(positions, heuristic2, marker="s", label="Heuristic 2")

plt.xticks(positions, stadiums)
plt.xlabel("Stadiums")
plt.ylabel("Heuristic Values")
plt.title("Comparison of Two A* Heuristics")

plt.legend()
plt.grid(True)

plt.savefig("../documentation/results/heuristic_comparison.png")

plt.show()