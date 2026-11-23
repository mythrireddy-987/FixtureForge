import sys
import os

from flask import Blueprint, request, jsonify
from datetime import date, timedelta

# Add the main FixtureForge folder to Python's search path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from algorithms.csp_scheduler import solve_csp

fixture_routes = Blueprint("fixture_routes", __name__)


def check_conflicts(fixtures):

    conflicts = []
    venue_slots = set()
    team_dates = {}

    for fixture in fixtures:


        venue_slot = (
            fixture["date"],
            fixture["time"],
            fixture["venue"]
        )

        if venue_slot in venue_slots:
            conflicts.append(
                f"Venue conflict: {fixture['venue']}"
            )

        venue_slots.add(venue_slot)

        for team in [fixture["team1"], fixture["team2"]]:

            if team not in team_dates:
                team_dates[team] = []

            team_dates[team].append(
                date(
                    int(fixture["date"][6:10]),
                    int(fixture["date"][3:5]),
                    int(fixture["date"][0:2])
                )
            )

    for team, dates in team_dates.items():

        dates.sort()

        for i in range(1, len(dates)):

            difference = (dates[i] - dates[i - 1]).days

            if difference < 2:
                conflicts.append(
                    f"Rest-day conflict: {team}"
                )

    return {
        "valid": len(conflicts) == 0,
        "conflicts": conflicts
    }


@fixture_routes.route("/generate-fixtures", methods=["POST"])
def generate_fixtures():

    data = request.get_json()
    teams = data.get("teams", [])

    teams = list(dict.fromkeys(
        team.strip() for team in teams if team.strip()
    ))

    if len(teams) < 2:
        return jsonify({
            "error": "At least two different teams are required"
        }), 400

    # Create all round-robin matches
    matches = []

    for i in range(len(teams)):

        for j in range(i + 1, len(teams)):

            matches.append({
                "team1": teams[i],
                "team2": teams[j]
            })

    venues = [
        "Stadium A",
        "Stadium B",
        "Stadium C"
    ]

    times = [
        "5:00 PM",
        "7:00 PM",
        "9:00 PM"
    ]

    # Generate possible match dates
    start_date = date.today()

    dates = [
        (start_date + timedelta(days=i * 2)).strftime("%d-%m-%Y")
        for i in range(len(matches) * 2)
    ]

    # Run CSP scheduler
    scheduled_matches = solve_csp(
        matches,
        dates,
        venues,
        times
    )

    if not scheduled_matches:

        return jsonify({
            "error": "No valid fixture schedule could be generated."
        }), 400

    fixtures = []

    for index, match in enumerate(scheduled_matches):

        fixtures.append({
            "match_number": index + 1,
            "round": index + 1,
            "team1": match["team1"],
            "team2": match["team2"],
            "date": match["date"],
            "time": match["time"],
            "venue": match["venue"]
        })

    validation = check_conflicts(fixtures)

    return jsonify({
        "total_matches": len(fixtures),
        "total_rounds": len(fixtures),
        "fixtures": fixtures,
        "validation": validation
    })