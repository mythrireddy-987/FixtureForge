import random
import math
import time
from datetime import datetime, timedelta


# Calculate scheduling conflicts
def calculate_cost(schedule):

    conflicts = 0
    team_dates = {}
    venue_slots = set()

    for match in schedule:

        team1 = match["team1"]
        team2 = match["team2"]
        match_date = datetime.strptime(
            match["date"], "%d-%m-%Y"
        ).date()

        venue_slot = (
            match["date"],
            match["time"],
            match["venue"]
        )

        if venue_slot in venue_slots:
            conflicts += 1

        venue_slots.add(venue_slot)

        for team in [team1, team2]:
            if team not in team_dates:
                team_dates[team] = []

            team_dates[team].append(match_date)

    for dates in team_dates.values():

        dates.sort()

        for i in range(1, len(dates)):

            difference = (dates[i] - dates[i - 1]).days

            if difference < 2:
                conflicts += 1

    return conflicts


# Create initial schedule
def create_initial_schedule(matches):
    return [match.copy() for match in matches]


# Generate neighbouring schedule
def generate_neighbour(schedule):

    new_schedule = [match.copy() for match in schedule]

    if len(new_schedule) < 2:
        return new_schedule

    index = random.randrange(len(new_schedule))

    current_date = datetime.strptime(
        new_schedule[index]["date"], "%d-%m-%Y"
    ).date()

    change = random.choice([-3, -2, 2, 3])

    new_date = current_date + timedelta(days=change)

    new_schedule[index]["date"] = new_date.strftime("%d-%m-%Y")

    return new_schedule


# Hill Climbing
def hill_climbing(matches):

    start_time = time.time()

    current_schedule = create_initial_schedule(matches)
    current_cost = calculate_cost(current_schedule)

    best_schedule = [match.copy() for match in current_schedule]
    best_cost = current_cost

    convergence = [best_cost]
    iterations = 0

    while iterations < 500 and best_cost > 0:

        new_schedule = generate_neighbour(current_schedule)
        new_cost = calculate_cost(new_schedule)

        if new_cost < current_cost:
            current_schedule = new_schedule
            current_cost = new_cost

        if current_cost < best_cost:

            best_schedule = [
                match.copy() for match in current_schedule
            ]

            best_cost = current_cost

        convergence.append(best_cost)
        iterations += 1

    return {
        "algorithm": "Hill Climbing",
        "schedule": best_schedule,
        "conflicts": best_cost,
        "iterations": iterations,
        "execution_time": time.time() - start_time,
        "convergence": convergence
    }


# Simulated Annealing
def simulated_annealing(matches):

    start_time = time.time()

    current_schedule = create_initial_schedule(matches)
    current_cost = calculate_cost(current_schedule)

    best_schedule = [match.copy() for match in current_schedule]
    best_cost = current_cost

    convergence = [best_cost]

    temperature = 100
    cooling_rate = 0.95
    iterations = 0

    while temperature > 0.1 and iterations < 500:

        new_schedule = generate_neighbour(current_schedule)
        new_cost = calculate_cost(new_schedule)

        difference = new_cost - current_cost

        if difference < 0 or random.random() < math.exp(
            -difference / temperature
        ):

            current_schedule = new_schedule
            current_cost = new_cost

        if current_cost < best_cost:

            best_schedule = [
                match.copy() for match in current_schedule
            ]

            best_cost = current_cost

        convergence.append(best_cost)

        temperature *= cooling_rate
        iterations += 1

        if best_cost == 0:
            break

    return {
        "algorithm": "Simulated Annealing",
        "schedule": best_schedule,
        "conflicts": best_cost,
        "iterations": iterations,
        "execution_time": time.time() - start_time,
        "convergence": convergence
    }