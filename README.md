FixtureForge – Sports Fixture Scheduler and Stadium Route Planner

About the Project

FixtureForge is a web-based sports fixture scheduling and stadium route-planning application. It helps users manage teams, generate fixtures, validate scheduling conflicts, and compare different pathfinding algorithms for stadium navigation.

Features

- Add and remove teams.
- Automatically generate sports fixtures.
- Validate fixture conflicts.
- Download fixtures as PDF.
- Find routes between stadiums.
- Compare five search algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search (UCS)
  - Greedy Best-First Search
  - A* Search
- Display travel cost, nodes expanded, and execution time.

Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript

Project Structure

- "algorithms/" – Search algorithm implementations.
- "backend/" – Flask backend and API routes.
- "database/" – Database-related files.
- "documentation/" – Project documentation.
- "frontend/" – User interface files.

Running the Project Locally

1. Install dependencies

pip install -r requirements.txt

2. Start the Flask backend

python backend/app.py

3. Open the application

Visit:
"http://127.0.0.1:5000"

Route Planning Example

For a route from Stadium A to Stadium D, the application compares the results of five search algorithms.

The optimal route in the current sample graph is:

Stadium A → Stadium C → Stadium D

Total travel cost: 8

Project Status

The application is working locally. Online deployment is the next stage.