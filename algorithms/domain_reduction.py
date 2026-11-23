from copy import deepcopy
from csp_scheduler import is_valid, ac3


# Three matches in a small league
matches = [
    {"team1": "RCB", "team2": "CSK"},
    {"team1": "RCB", "team2": "MI"},
    {"team1": "CSK", "team2": "MI"}
]

dates = [
    "01-12-2026",
    "02-12-2026",
    "03-12-2026"
]

venues = ["Stadium A", "Stadium B"]
times = ["10:00 AM", "02:00 PM"]


# Create the initial domain for each match
domains = {}

for index, match in enumerate(matches):
    domains[index] = []

    for date in dates:
        for venue in venues:
            for time in times:
                domains[index].append({
                    "team1": match["team1"],
                    "team2": match["team2"],
                    "date": date,
                    "venue": venue,
                    "time": time
                })


print("DOMAIN REDUCTION EXPERIMENT")
print("-" * 50)

for index in domains:
    print(f"Match {index + 1}: {len(domains[index])} possible values")


# Apply Forward Checking using one assigned value
forward_domains = deepcopy(domains)

assigned_match = forward_domains[0][0]

for index in forward_domains:
    if index != 0:
        forward_domains[index] = [
            option for option in forward_domains[index]
            if is_valid(option, [assigned_match])
        ]

print("\nAfter Forward Checking:")

for index in forward_domains:
    print(f"Match {index + 1}: {len(forward_domains[index])} possible values")


# Apply AC-3 to the original domains
ac3_domains = deepcopy(domains)

ac3(ac3_domains, matches)

print("\nAfter AC-3:")

for index in ac3_domains:
    print(f"Match {index + 1}: {len(ac3_domains[index])} possible values")