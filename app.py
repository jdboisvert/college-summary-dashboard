from flask import Flask, render_template
from flask_pymongo import PyMongo

from utils import datastore

app = Flask(__name__, static_url_path="/static")

# TODO Make a setting
app.config[
    "MONGO_URI"
] = "mongodb://127.0.0.1:27017/collegeDashboardDB/?directConnection=true&serverSelectionTimeoutMS=200"

mongodb_client = PyMongo(app)
datastore.db = mongodb_client.db


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
