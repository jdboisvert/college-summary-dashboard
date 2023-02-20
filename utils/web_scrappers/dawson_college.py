import logging

from constants import College
from utils.dataclasses.dashboard import CollegeMetrics

from utils.datastore import CollegeMetricsDataStore
from dawson_college_pyscrapper.scrapper import scrape as dawson_college_scrape

logger = logging.getLogger(__name__)


class DawsonCollegeWebsiteScrapper:
    """
    A web scrapper used to get program details from Dawson College.
    """

    def scrape(self):
        """
        Scrapes the Dawson College website and saves it to the database.
        """
        general_metrics = dawson_college_scrape()
        college_metrics = CollegeMetrics(
            date=general_metrics.date,
            college=College.DAWSON_COLLEGE.name,
            total_programs_offered=general_metrics.total_programs_offered,
            number_of_programs=general_metrics.number_of_programs,
            number_of_profiles=general_metrics.number_of_profiles,
            number_of_disciplines=general_metrics.number_of_disciplines,
            number_of_special_studies=general_metrics.number_of_special_studies,
            number_of_general_studies=general_metrics.number_of_general_studies,
            total_year_counts=general_metrics.total_year_counts,
            programs=general_metrics.programs,
            number_of_students=general_metrics.number_of_students,
            number_of_faculty=general_metrics.number_of_faculty,
        )
        
        logger.info(f"Saving college metrics: {college_metrics}")
        
        CollegeMetricsDataStore.save(
            college_metrics=college_metrics
        )
