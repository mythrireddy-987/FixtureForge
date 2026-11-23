from fixture_optimizer import (
    calculate_cost,
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

baseline_cost = calculate_cost(matches)

hill_result = hill_climbing(matches)
annealing_result = simulated_annealing(matches)

print("\nOPTIMISATION COMPARISON")
print("-" * 75)

print(
    f"{'Method':<25}"
    f"{'Conflicts':<15}"
    f"{'Iterations':<15}"
    f"{'Time (seconds)':<15}"
)

print("-" * 75)

print(f"{'Baseline':<25}{baseline_cost:<15}{0:<15}{0:<15.6f}")

print(
    f"{'Hill Climbing':<25}"
    f"{hill_result['conflicts']:<15}"
    f"{hill_result['iterations']:<15}"
    f"{hill_result['execution_time']:<15.6f}"
)

print(
    f"{'Simulated Annealing':<25}"
    f"{annealing_result['conflicts']:<15}"
    f"{annealing_result['iterations']:<15}"
    f"{annealing_result['execution_time']:<15.6f}"
)