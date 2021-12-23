from typing import List

from utils.dataclasses import CollegeMetrics


class CollegeMetricsDataStore:
    def __init__(self):
        # TODO create connection to datastore.
        pass

    def get_latest(self) -> CollegeMetrics:
        pass

    def get_all(self) -> List[CollegeMetrics]:
        """
        :return: A list of CollegeMetrics from newest to oldest.
        """
        pass

    def save(self, college_metrics: CollegeMetrics):
        pass