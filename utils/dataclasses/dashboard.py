from dataclasses import dataclass
from datetime import datetime
from typing import List

from dawson_college_pyscrapper.models import Program

@dataclass(frozen=True)
class CollegeMetrics:
    college: str
    date: datetime
    total_programs_offered: int

    number_of_programs: int
    number_of_profiles: int
    number_of_disciplines: int
    number_of_special_studies: int
    number_of_general_studies: int
    number_of_students: int
    number_of_faculty: int

    total_year_counts: dict
    programs: List[Program]

    def __post_init__(self):
        for i in range(len(self.programs)):
            if not isinstance(self.programs[i], Program):
                self.programs[i] = Program(**{**self.programs[i]})

    @property
    def number_of_students_per_faculty(self) -> float:
        return round((self.number_of_students / self.number_of_faculty), 2)

    @property
    def programs_sorted(self) -> List[Program]:
        return sorted(
            self.programs,
            key=lambda program: datetime.strptime(program.modified_date, "%B %d, %Y"),
            reverse=True,
        )
