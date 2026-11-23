from datetime import datetime
from time import perf_counter


matches = [
    {"team1": "RCB", "team2": "CSK"},
    {"team1": "RCB", "team2": "MI"},
    {"team1": "CSK", "team2": "MI"},
    {"team1": "RCB", "team2": "KKR"},
    {"team1": "CSK", "team2": "KKR"},
    {"team1": "MI", "team2": "KKR"}
]

dates = [
    "01-12-2026",
    "03-12-2026",
    "05-12-2026",
    "07-12-2026"
]

venues = ["Stadium A", "Stadium B"]
times = ["10:00 AM", "02:00 PM"]


def is_valid(option, assignment):
    option_date = datetime.strptime(
        option["date"], "%d-%m-%Y"
    ).date()

    for scheduled in assignment:
        scheduled_date = datetime.strptime(
            scheduled["date"], "%d-%m-%Y"
        ).date()

        if (
            option["date"] == scheduled["date"]
            and option["time"] == scheduled["time"]
            and option["venue"] == scheduled["venue"]
        ):
            return False

        teams1 = {option["team1"], option["team2"]}
        teams2 = {scheduled["team1"], scheduled["team2"]}

        if teams1.intersection(teams2):
            if abs((option_date - scheduled_date).days) < 2:
                return False

    return True


def create_domains():
    domains = {}

    for i, match in enumerate(matches):
        domains[i] = []

        for date in dates:
            for venue in venues:
                for time in times:
                    domains[i].append({
                        "team1": match["team1"],
                        "team2": match["team2"],
                        "date": date,
                        "venue": venue,
                        "time": time
                    })

    return domains


def solve(mode):
    domains = create_domains()
    assignment = {}
    backtracks = 0

    def choose_variable(unassigned):
        if mode == "Plain":
            return unassigned[0]

        if mode == "MRV":
            return min(unassigned, key=lambda v: len(domains[v]))

        if mode == "Degree":
            return max(
                unassigned,
                key=lambda v: sum(
                    bool(
                        {matches[v]["team1"], matches[v]["team2"]}
                        & {matches[o]["team1"], matches[o]["team2"]}
                    )
                    for o in unassigned if o != v
                )
            )

        return min(unassigned, key=lambda v: len(domains[v]))

    def backtrack():
        nonlocal backtracks

        if len(assignment) == len(matches):
            return True

        unassigned = [
            v for v in domains if v not in assignment
        ]

        variable = choose_variable(unassigned)

        values = domains[variable]

        if mode == "LCV":
            values = sorted(
                values,
                key=lambda value: sum(
                    not is_valid(value, [other])
                    for v in unassigned if v != variable
                    for other in domains[v]
                )
            )

        for value in values:
            if is_valid(value, list(assignment.values())):
                assignment[variable] = value

                if backtrack():
                    return True

                assignment.pop(variable)

        backtracks += 1
        return False

    start = perf_counter()
    success = backtrack()
    elapsed = perf_counter() - start

    return success, backtracks, elapsed


print("BACKTRACKING COMPARISON")
print("-" * 65)
print(f"{'Method':<15}{'Backtracks':<15}{'Time (seconds)':<20}")
print("-" * 65)

for method in ["Plain", "MRV", "Degree", "LCV"]:
    success, backtracks, elapsed = solve(method)

    print(
        f"{method:<15}{backtracks:<15}{elapsed:<20.6f}"
    )

    if not success:
        print("No valid schedule found.")