from dataclasses import dataclass


@dataclass(frozen=True)
class Program:
    name: str
    modified_date: str
    type: str
    url: str


@dataclass(frozen=True)
class CollegeMetrics:
    college: str
    date: str
    total_programs_offered: int

    number_of_programs: int
    number_of_profiles: int
    number_of_disciplines: int
    number_of_special_studies: int
    number_of_general_studies: int
    number_of_students: int
    number_of_faculty: int

    total_year_counts: dict
    programs: str

    @property
    def number_of_students_per_faculty(self) -> float:
        return round((self.number_of_students / self.number_of_faculty), 2)




