import matplotlib.pyplot as plt

from fixture_optimizer import (
    hill_climbing,
    simulated_annealing
)


matches = [
    {
        "team1": "Team A",
        "team2": "Team B",
        "date": "01-12-2026",
        "time": "5:00 PM",
        "venue": "Stadium A"
    },
    {
        "team1": "Team A",
        "team2": "Team C",
        "date": "02-12-2026",
        "time": "7:00 PM",
        "venue": "Stadium B"
    },
    {
        "team1": "Team B",
        "team2": "Team C",
        "date": "03-12-2026",
        "time": "5:00 PM",
        "venue": "Stadium A"
    }
]


hill = hill_climbing(matches)
annealing = simulated_annealing(matches)

plt.plot(
    range(len(hill["convergence"])),
    hill["convergence"],
    label="Hill Climbing"
)

plt.plot(
    range(len(annealing["convergence"])),
    annealing["convergence"],
    label="Simulated Annealing"
)

plt.xlabel("Iterations")
plt.ylabel("Number of Conflicts")
plt.title("Fixture Scheduling Optimization - Convergence Plot")

plt.legend()
plt.grid(True)

plt.savefig("convergence_plot.png")
plt.show()

print("Convergence plot saved successfully!")