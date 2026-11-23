Team Travel Route – State-Space Problem Formulation

1. Initial State

The starting stadium from which a team begins its journey.

2. Goal State

The destination stadium where the team must reach.

3. States

Each stadium represents a state in the search problem.

4. Actions

Moving from one stadium to another through an available travel route.

5. Transition Model

Moving along a route changes the team's current location from one stadium to another.

6. Path Cost

The total travel cost between the starting stadium and destination stadium. In FixtureForge, the route costs represent travel distances.

7. Search Algorithms

The following algorithms are used to find routes:

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Greedy Best-First Search
- A* Search

Conclusion

The team travel problem is represented as a state-space search problem in which stadiums are states and travel routes are actions. Search algorithms help identify suitable routes between stadiums.
# Fixture Scheduling – CSP Problem Formulation

## 1. Variables
Each match in the league is considered a variable.
For example:
- M1 = Team A vs Team B
- M2 = Team A vs Team C
- M3 = Team B vs Team C

## 2. Domains
Each match can be assigned:
- An available date
- An available venue
- An available time slot

The domain consists of all possible combinations of these options.

## 3. Constraints

Hard constraints:

1. A team must have at least 2 days of rest between its matches.
2. Two matches cannot use the same venue at the same date and time.
3. Every match must be assigned a valid date, venue, and time.

## 4. Initial State
All matches are unassigned, and possible dates, venues, and time slots are available.

## 5. Goal State
All matches are assigned dates, venues, and time slots while satisfying every constraint.