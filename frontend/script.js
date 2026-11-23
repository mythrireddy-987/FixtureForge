let teams = [];
let totalGeneratedMatches = 0;


// ADD TEAM
function addTeam() {
    const input = document.getElementById("teamName");
    const teamName = input.value.trim();

    if (teamName === "") {
        alert("Please enter a team name!");
        return;
    }

    if (teams.some(team =>
        team.toLowerCase() === teamName.toLowerCase()
    )) {
        alert("This team already exists!");
        return;
    }

    teams.push(teamName);
    input.value = "";

    displayTeams();
    updateDashboard();
}


// DISPLAY TEAMS
function displayTeams() {
    const teamList = document.getElementById("teamList");
    teamList.innerHTML = "";

    teams.forEach((team, index) => {
        const li = document.createElement("li");

        li.innerHTML = `
            ${team}
            <button onclick="removeTeam(${index})">Remove</button>
        `;

        teamList.appendChild(li);
    });
}


// REMOVE TEAM
function removeTeam(index) {
    teams.splice(index, 1);

    displayTeams();
    updateDashboard();
}


// UPDATE DASHBOARD
function updateDashboard() {
    document.getElementById("totalTeams").textContent = teams.length;

    document.getElementById("totalMatches").textContent =
        totalGeneratedMatches;
}


// GENERATE FIXTURES
async function generateFixtures() {

    if (teams.length < 2) {
        alert("Please add at least two teams!");
        return;
    }

    try {
        const response = await fetch(
            "/generate-fixtures",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ teams: teams })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.error || "Unable to generate fixtures.");
            return;
        }

        const fixtureList = document.getElementById("fixtureList");
        fixtureList.innerHTML = "";

        // DISPLAY FIXTURES
        data.fixtures.forEach(fixture => {

            const div = document.createElement("div");
            div.className = "fixture-card";

            div.innerHTML = `
                <h3>Match ${fixture.match_number}</h3>
                <p><strong>Round:</strong> ${fixture.round}</p>
                <p><strong>Teams:</strong> ${fixture.team1} vs ${fixture.team2}</p>
                <p><strong>Date:</strong> ${fixture.date}</p>
                <p><strong>Time:</strong> ${fixture.time}</p>
                <p><strong>Venue:</strong> ${fixture.venue}</p>
            `;

            fixtureList.appendChild(div);
        });


        // DISPLAY CONFLICT VALIDATION
        const validationMessage =
            document.getElementById("validationMessage");

        if (data.validation && data.validation.valid) {

            validationMessage.innerHTML = `
                <div style="
                    background:#dcfce7;
                    color:#166534;
                    padding:15px;
                    border-radius:8px;
                    margin:15px 0;
                    font-weight:bold;
                ">
                    No Conflicts Found! All Fixtures Are Valid.
                </div>
            `;

        } else if (data.validation) {

            validationMessage.innerHTML = `
                <div style="
                    background:#fee2e2;
                    color:#991b1b;
                    padding:15px;
                    border-radius:8px;
                    margin:15px 0;
                ">
                    <strong>Conflicts Detected!</strong>
                    <ul>
                        ${data.validation.conflicts.map(
                            conflict => `<li>${conflict}</li>`
                        ).join("")}
                    </ul>
                </div>
            `;

        } else {

            validationMessage.textContent =
                "Validation information is unavailable.";
        }

        totalGeneratedMatches = data.fixtures.length;
        updateDashboard();

    } catch (error) {

        alert(
            "Backend connection failed. Please start the Python server."
        );

        console.error("Fixture generation error:", error);
    }
}


// DOWNLOAD FIXTURES AS PDF
function downloadFixtures() {

    const fixtureList = document.getElementById("fixtureList");

    if (fixtureList.innerHTML.trim() === "") {
        alert("Please generate fixtures before downloading!");
        return;
    }

    const printWindow = window.open("", "_blank");

    if (!printWindow) {
        alert("Please allow pop-ups in your browser to download the PDF.");
        return;
    }

    const validationMessage =
        document.getElementById("validationMessage").innerHTML;

    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>FixtureForge - Match Fixtures</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 30px;
                    color: #1e293b;
                }

                h1 {
                    text-align: center;
                    color: #1e40af;
                    margin-bottom: 5px;
                }

                h2 {
                    text-align: center;
                    color: #475569;
                    margin-bottom: 30px;
                }

                .fixture-card {
                    border: 1px solid #cbd5e1;
                    border-left: 5px solid #2563eb;
                    padding: 15px;
                    margin-bottom: 15px;
                    border-radius: 8px;
                    page-break-inside: avoid;
                }

                .fixture-card h3 {
                    color: #1e40af;
                }

                .fixture-card p {
                    margin: 8px 0;
                }
            </style>
        </head>

        <body>
            <h1>FixtureForge</h1>
            <h2>Sports Match Fixtures</h2>

            ${validationMessage}
            ${fixtureList.innerHTML}

        </body>
        </html>
    `);

    printWindow.document.close();

    printWindow.onload = function () {
        printWindow.focus();
        printWindow.print();
    };
}


// STADIUM TRAVEL ROUTE PLANNER

async function findRoute() {

    const start =
        document.getElementById("startStadium").value;

    const goal =
        document.getElementById("goalStadium").value;

    const algorithm =
        document.getElementById("searchAlgorithm").value;

    const resultsDiv =
        document.getElementById("routeResults");


    // CHECK STADIUM SELECTION
    if (start === goal) {
        resultsDiv.innerHTML =
            "<p>Please select two different stadiums.</p>";
        return;
    }

    resultsDiv.innerHTML =
        "<p>Searching for the best route...</p>";


    try {

        // DEBUGGING MESSAGE
        console.log(
            "Sending route request:",
            start,
            goal,
            algorithm
        );


        // SEND REQUEST TO FLASK BACKEND
        const response = await fetch("/find-route",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    start: start,
                    goal: goal,
                    algorithm: algorithm
                })
            }
        );


        // CHECK SERVER RESPONSE
        console.log(
            "Route response status:",
            response.status
        );

        const data = await response.json();


        if (!response.ok) {

            resultsDiv.innerHTML = `
                <p>${data.error || "Unable to find route."}</p>
            `;

            return;
        }


        // DISPLAY ROUTE RESULTS
        let html = "<h3>Route Search Results</h3>";

        data.results.forEach(result => {

            html += `
                <div class="route-result-card">

                    <h4>${result.algorithm}</h4>

                    <p>
                        <strong>Route:</strong>
                        ${
                            result.route
                                ? result.route.join(" → ")
                                : "No route found"
                        }
                    </p>

                    <p>
                        <strong>Travel Cost:</strong>
                        ${
                            result.travel_cost ?? "Not available"
                        }
                    </p>

                    <p>
                        <strong>Nodes Expanded:</strong>
                        ${
                            result.nodes_expanded ?? "Not available"
                        }
                    </p>

                    <p>
                        <strong>Execution Time:</strong>
                        ${
                            (result.execution_time * 1000).toFixed(4)
                        } ms
                    </p>

                </div>
            `;
        });

        resultsDiv.innerHTML = html;


    } catch (error) {

        resultsDiv.innerHTML = `
            <p>
                Backend connection failed.
                Please check the Flask server.
            </p>
        `;

        console.error("Route search error:", error);
    }
}