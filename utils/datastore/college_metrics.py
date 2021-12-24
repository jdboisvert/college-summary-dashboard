from typing import List

from utils.dataclasses import CollegeMetrics

from utils.datastore import db


class CollegeMetricsDataStore:
    @classmethod
    def get_latest(cls) -> CollegeMetrics:
        result = db.college_metrics.find_one({}, sort=[("$natural", -1)])

        return CollegeMetrics(**result)

    @classmethod
    def get_all(cls) -> List[CollegeMetrics]:
        results = db.college_metrics.find({}).sort([("$natural", -1)])

        return [CollegeMetrics(**result) for result in results]

    @classmethod
    def save(cls, college_metrics: CollegeMetrics):
        db.college_metrics.insert_one(**college_metrics.__dict__)
