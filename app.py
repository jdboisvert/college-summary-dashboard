import click
from flask import Flask, render_template
from flask_pymongo import pymongo
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import os

from exceptions.dashboard import NoCollegeMetricsFoundError
from utils import DawsonCollegeWebsiteScrapper
from utils.datastore import CollegeMetricsDataStore

import logging

logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path="/static")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

mongodb_client = pymongo.MongoClient(app.config["MONGO_URI"])
db = mongodb_client.get_database('collegeDashboardDB')
CollegeMetricsDataStore.db = db


def scrape_website():
    logger.info("About to scrap website for college details.")
    DawsonCollegeWebsiteScrapper().scrape()
    logger.info("College scrapping completed with no errors.")


if os.getenv("IS_SCHEDULED_SCRAPPING_ENABLED", "false").lower() in ("true", "1", "t"):
    background_scheduler = BackgroundScheduler(
        daemon=True, timezone=os.getenv("SCHEDULER_TIMEZONE")
    )
    background_scheduler.add_job(scrape_website, "interval", hours=12)

    background_scheduler.start()
    atexit.register(lambda: background_scheduler.shutdown())


@app.cli.command("scrape")
def scrap():
    click.echo("Scrapping Dawson College website ...")
    scrape_website()
    click.echo("Scrapping Complete.")


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/", methods=["GET"])
def dashboard():
    try:
        college_metrics = CollegeMetricsDataStore.get_latest()

        return render_template("dashboard.html", college_metrics=college_metrics)

    except NoCollegeMetricsFoundError:
        logger.error("No college metrics were found.")

        return render_template("empty-dashboard.html")
