from flask import Flask, render_template
from flask_pymongo import PyMongo

from utils.datastore import CollegeMetricsDataStore
from utils.web_scrappers import DawsonCollegeWebsiteScrapper

app = Flask(__name__, static_url_path="/static")

# TODO Make a setting
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/collegeDashboardDB"

mongodb_client = PyMongo(app)
CollegeMetricsDataStore.db = mongodb_client.db


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/", methods=["GET"])
def dashboard():
    # TODO Used just for initial testing to be removed.
    # DawsonCollegeWebsiteScrapper().scrap()
    college_metrics = CollegeMetricsDataStore.get_latest()

    return render_template("dashboard.html", college_metrics=college_metrics)


if __name__ == "__main__":
    app.run()
