from typing import List

from constants import College
from exceptions.dashboard import NoCollegeMetricsFoundError
from utils.dataclasses import CollegeMetrics


class CollegeMetricsDataStore:
    db = None

    @classmethod
    def get_latest(cls, college: College = College.DAWSON_COLLEGE) -> CollegeMetrics:
        result = cls.db.college_metrics.find_one(
            {"college": college.name}, sort=[("$natural", -1)]
        )

        if not result:
            raise NoCollegeMetricsFoundError()

        result.pop("_id")
        return CollegeMetrics(**result)

    @classmethod
    def get_all(cls, college: College = College.DAWSON_COLLEGE) -> List[CollegeMetrics]:
        results = cls.db.college_metrics.find({"college": college.name}).sort(
            [("$natural", -1)]
        )

        if not results:
            raise NoCollegeMetricsFoundError()

        return [CollegeMetrics(**result) for result in results]

    @classmethod
    def save(cls, college_metrics: CollegeMetrics):
        college_metrics_dict = {
            **college_metrics.__dict__,
            "programs": [program.__dict__ for program in college_metrics.programs],
        }

        cls.db.college_metrics.insert_one(college_metrics_dict)
