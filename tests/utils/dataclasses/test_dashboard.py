from datetime import datetime

from constants import College
from utils.dataclasses import CollegeMetrics


def test_number_of_students_per_faculty_students_higher_than_faculty():
    college_metrics = CollegeMetrics(
        college=College.DAWSON_COLLEGE.name,
        date=datetime.now().isoformat(),
        total_programs_offered=30,
        number_of_programs=10,
        number_of_profiles=10,
        number_of_disciplines=3,
        number_of_special_studies=3,
        number_of_general_studies=4,
        number_of_students=20,
        number_of_faculty=10,
        total_year_counts={},
        programs="",
    )
    assert college_metrics.number_of_students_per_faculty == 2


def test_number_of_students_per_faculty_faculty_higher_than_students():
    college_metrics = CollegeMetrics(
        college=College.DAWSON_COLLEGE.name,
        date=datetime.now().isoformat(),
        total_programs_offered=30,
        number_of_programs=10,
        number_of_profiles=10,
        number_of_disciplines=3,
        number_of_special_studies=3,
        number_of_general_studies=4,
        number_of_students=10,
        number_of_faculty=20,
        total_year_counts={},
        programs="",
    )
    assert college_metrics.number_of_students_per_faculty == 0.5


def test_number_of_students_per_faculty_students_and_faculty_are_the_same():
    college_metrics = CollegeMetrics(
        college=College.DAWSON_COLLEGE.name,
        date=datetime.now().isoformat(),
        total_programs_offered=30,
        number_of_programs=10,
        number_of_profiles=10,
        number_of_disciplines=3,
        number_of_special_studies=3,
        number_of_general_studies=4,
        number_of_students=10,
        number_of_faculty=10,
        total_year_counts={},
        programs="",
    )
    assert college_metrics.number_of_students_per_faculty == 1


def test_number_of_students_per_faculty_rounding():
    college_metrics = CollegeMetrics(
        college=College.DAWSON_COLLEGE.name,
        date=datetime.now().isoformat(),
        total_programs_offered=30,
        number_of_programs=10,
        number_of_profiles=10,
        number_of_disciplines=3,
        number_of_special_studies=3,
        number_of_general_studies=4,
        number_of_students=8000,
        number_of_faculty=9000,
        total_year_counts={},
        programs="",
    )

    # 8000 / 9000 = 0.8888888...8
    assert college_metrics.number_of_students_per_faculty == 0.89
