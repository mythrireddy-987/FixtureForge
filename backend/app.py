import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes import fixture_routes
from route_api import route_api

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_FOLDER = os.path.join(PROJECT_ROOT, "frontend")
print("FRONTEND FOLDER:", FRONTEND_FOLDER)
print("INDEX EXISTS:", os.path.exists(os.path.join(FRONTEND_FOLDER, "index.html")))

app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER,
    static_url_path="/static")


app.register_blueprint(fixture_routes)
app.register_blueprint(route_api)


@app.route("/")
def home():
    print("FIXTUREFORGE DASHBOARD ROUTE OPENED")
    return send_from_directory(FRONTEND_FOLDER, "index.html")

if __name__ == "__main__":
    app.run(debug=True)