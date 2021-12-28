from typing import List

from utils.dataclasses import CollegeMetrics


class CollegeMetricsDataStore:
    db = None

    @classmethod
    def get_latest(cls) -> CollegeMetrics:
        result = cls.db.college_metrics.find_one({}, sort=[("$natural", -1)])
        result.pop("_id")

        return CollegeMetrics(**result)

    @classmethod
    def get_all(cls) -> List[CollegeMetrics]:
        results = cls.db.college_metrics.find({}).sort([("$natural", -1)])

        return [CollegeMetrics(**result) for result in results]

    @classmethod
    def save(cls, college_metrics: CollegeMetrics):
        college_metrics_dict = {
            **college_metrics.__dict__,
            "programs": [program.__dict__ for program in college_metrics.programs],
        }

        cls.db.college_metrics.insert_one(college_metrics_dict)
