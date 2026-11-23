from datetime import datetime
from collections import deque


# Check whether two matches can be scheduled together
def is_valid(match, assignment):

    match_date = datetime.strptime(
        match["date"], "%d-%m-%Y"
    ).date()

    for scheduled in assignment:

        scheduled_date = datetime.strptime(
            scheduled["date"], "%d-%m-%Y"
        ).date()

        # Venue conflict
        if (
            match["date"] == scheduled["date"]
            and match["time"] == scheduled["time"]
            and match["venue"] == scheduled["venue"]
        ):
            return False

        # Team rest-period constraint
        teams1 = {match["team1"], match["team2"]}
        teams2 = {scheduled["team1"], scheduled["team2"]}

        if teams1.intersection(teams2):

            difference = abs(
                (match_date - scheduled_date).days
            )

            if difference < 2:
                return False

    return True


# Degree Heuristic
def degree_heuristic(variable, unassigned, matches):

    teams = {
        matches[variable]["team1"],
        matches[variable]["team2"]
    }

    degree = 0

    for other in unassigned:

        if other == variable:
            continue

        other_teams = {
            matches[other]["team1"],
            matches[other]["team2"]
        }

        if teams.intersection(other_teams):
            degree += 1

    return degree


# AC-3 Algorithm
def ac3(domains, matches):

    queue = deque()

    for i in domains:
        for j in domains:
            if i != j:
                queue.append((i, j))

    while queue:

        xi, xj = queue.popleft()

        revised = False

        new_domain = []

        for value in domains[xi]:

            supported = any(
                is_valid(value, [other])
                for other in domains[xj]
            )

            if supported:
                new_domain.append(value)
            else:
                revised = True

        if revised:

            domains[xi] = new_domain

            if not domains[xi]:
                return False

            for neighbour in domains:

                if neighbour != xi and neighbour != xj:
                    queue.append((neighbour, xi))

    return True


# CSP Solver
def solve_csp(matches, dates, venues, times):

    domains = {}

    # Generate domains for every match
    for index, match in enumerate(matches):

        domains[index] = []

        for date in dates:
            for venue in venues:
                for time in times:

                    option = {
                        "team1": match["team1"],
                        "team2": match["team2"],
                        "date": date,
                        "venue": venue,
                        "time": time
                    }

                    domains[index].append(option)

    # Apply AC-3 before backtracking
    if not ac3(domains, matches):
        return None

    assignment = {}

    def backtrack():

        # All matches assigned
        if len(assignment) == len(matches):
            return True

        unassigned = [
            i for i in domains
            if i not in assignment
        ]

        # MRV + Degree Heuristic
        variable = min(
            unassigned,
            key=lambda i: (
                len(domains[i]),
                -degree_heuristic(i, unassigned, matches)
            )
        )

        # LCV: Try the value that rules out the fewest
        # values from other unassigned variables first.
        def lcv_score(option):

            score = 0

            for other in unassigned:

                if other == variable:
                    continue

                for other_option in domains[other]:

                    if not is_valid(option, [other_option]):
                        score += 1

            return score

        ordered_values = sorted(
            domains[variable],
            key=lcv_score
        )

        for option in ordered_values:

            current_schedule = list(assignment.values())

            if is_valid(option, current_schedule):

                assignment[variable] = option

                # Forward Checking
                saved_domains = {
                    key: value.copy()
                    for key, value in domains.items()
                }

                failure = False

                for other in unassigned:

                    if other == variable:
                        continue

                    domains[other] = [
                        value for value in domains[other]
                        if is_valid(value, [option])
                    ]

                    if not domains[other]:
                        failure = True
                        break

                # Apply AC-3 after forward checking
                if not failure and ac3(domains, matches):

                    if backtrack():
                        return True

                # Backtrack
                assignment.pop(variable)

                domains.clear()
                domains.update(saved_domains)

        return False

    if backtrack():
        return list(assignment.values())

    return None


# Test the CSP Scheduler independently
if __name__ == "__main__":

    matches = [
        {"team1": "Team A", "team2": "Team B"},
        {"team1": "Team A", "team2": "Team C"},
        {"team1": "Team B", "team2": "Team C"}
    ]

    dates = [
        "01-12-2026",
        "03-12-2026",
        "05-12-2026"
    ]

    venues = [
        "Stadium A",
        "Stadium B"
    ]

    times = [
        "10:00 AM",
        "02:00 PM"
    ]

    result = solve_csp(
        matches,
        dates,
        venues,
        times
    )

    print("\nCSP FIXTURE SCHEDULER")
    print("-" * 60)

    if result:

        for match in result:

            print(
                match["team1"], "vs", match["team2"],
                "| Date:", match["date"],
                "| Time:", match["time"],
                "| Venue:", match["venue"]
            )

        print("\nValid schedule generated successfully!")

    else:

        print("No valid fixture schedule found.")