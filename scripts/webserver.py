# scripts/webserver.py
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Mock LinkedIn Page</h1><p>This is a test profile page.</p>"

@app.route("/profile")
@app.route("/job")
@app.route("/connect")
@app.route("/search")
def simulate():
    ua = request.headers.get("User-Agent", "unknown")
    return f"<h2>Endpoint: {request.path}</h2><p>Your agent is: {ua}</p>", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
