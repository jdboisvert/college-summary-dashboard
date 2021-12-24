from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup, Tag
import json
import pandas as pd
import logging

from pandas import DataFrame

from constants import College
from constants.dawson_college import PROGRAMS_LISTING_URL, MAIN_WEBSITE_URL
from utils.dataclasses.dashboard import Program, CollegeMetrics
from utils.dataclasses.dawson_college import ProgramPageData

from utils.datastore import CollegeMetricsDataStore

logger = logging.getLogger(__name__)


class DawsonCollegeWebsiteScrapper:
    """
    A web scrapper used to get program details from Dawson College.
    """

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "referrer": "https://google.com",
    }

    def __get_soup_of_page(self, url) -> BeautifulSoup:
        response = requests.get(url, headers=self.headers)

        if not response.ok:
            # TODO Make custom exception
            raise Exception("Could not get page details")

        return BeautifulSoup(response.text.strip(), "lxml")

    def __get_date_of_modification(self, html_soup: "BeautifulSoup") -> str:
        date_modified_text = html_soup.find(class_="page-mod-date").contents[0].strip()

        return date_modified_text.replace("Last Modified: ", "")

    def __def_parse_program_page(self, program_url: str) -> ProgramPageData:
        html_soup = self.__get_soup_of_page(program_url)

        date_modified = self.__get_date_of_modification(html_soup=html_soup)

        return ProgramPageData(date=date_modified)

    def __get_program_details(self, program_url: str, listed_program: Tag) -> Program:
        program_page_data = self.__def_parse_program_page(program_url)
        program_type = listed_program.find(class_="program-type")
        if program_type:
            program_type_data = program_type.contents[0].strip()
            program_name = (
                listed_program.find(class_="program-name").find("a").contents[0].strip()
            )

            return Program(
                name=program_name,
                modified_date=program_page_data.date,
                type=program_type_data,
                url=program_url,
            )

    def __get_number_of_type(self, data_frame: DataFrame, wanted_type: str):
        query = data_frame["type"] == wanted_type

        return len(data_frame[query])

    def get_programs(self) -> List[Program]:
        all_programs_listed_html_soup = self.__get_soup_of_page(PROGRAMS_LISTING_URL)

        entry_content = all_programs_listed_html_soup.find(class_="entry-content")
        listed_programs = entry_content.find_all("tr")

        programs = []
        for listed_program in listed_programs:
            program_name = listed_program.find(class_="program-name")
            if not programs:
                continue

            program_path = program_name.find("a")["href"]
            if program_path == "/programs/general-education":
                # Not an actual program.
                continue

            program_url = f"{MAIN_WEBSITE_URL}/{program_path}"

            try:
                programs.append(
                    self.__get_program_details(
                        program_url=program_url, listed_program=listed_program
                    )
                )
            except Exception as e:
                logger.error(f"Error occurred while get details from {program_url}")
                continue

        return programs

    def get_total_number_of_students(self) -> int:
        # TODO should use something more reliable than google here.
        soup = self.__get_soup_of_page(
            "https://www.google.com/search?q=dawson+college+number+of+students&stick=H4sIAAAAAAAAAOPgE-LUz9U3MLTMKjbV0s8ot9JPzs_JSU0uyczP088vSk_My6xKBHGKrfJKc5NSixTy0xSKS0pTUvNKihexKqYklhfn5ymANaWnKmCqAQDR74rvYgAAAA&sa=X&ved=2ahUKEwjXvq6b97XjAhUaQ80KHTRfCb8Q6BMoADAgegQIGhAC&biw=1156&bih=754"
        )

        tag = soup.find(class_="Z0LcW")
        content = tag.contents[0].strip()

        return int(content.replace(",", ""))

    def get_total_number_of_faculty(self):
        params = {"position": "Faculty", "search": "Search"}

        # This is needed to allow the post to go through.
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 "
            "Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = requests.post(
            f"{MAIN_WEBSITE_URL}/phone-directory", data=params, headers=headers
        )
        response_soup = BeautifulSoup(response.text, "html.parser")

        tags = response_soup.find_all("b")

        return int(tags[0].contents[0])

    def scrap(self):
        number_of_students = self.get_total_number_of_students()
        number_of_faculty = self.get_total_number_of_faculty()

        programs = self.get_programs()
        programs_data_frame = pd.DataFrame(programs)

        # Change date to actual Timestamp type
        programs_data_frame["date"] = pd.to_datetime(programs_data_frame["date"])

        total_programs_offered = len(programs_data_frame)
        number_of_programs = self.__get_number_of_type(programs_data_frame, "Program")
        number_of_profiles = self.__get_number_of_type(programs_data_frame, "Profile")
        number_of_disciplines = self.__get_number_of_type(
            programs_data_frame, "Discipline"
        )
        number_of_special_studies = self.__get_number_of_type(
            programs_data_frame, "Special Area of Study"
        )
        number_of_general_education = self.__get_number_of_type(
            programs_data_frame, "General Education"
        )

        years = []
        for date in programs_data_frame["date"]:
            years.append(date.year)

        programs_data_frame["year"] = years
        total_year_counts = programs_data_frame["year"].value_counts()

        newest = programs_data_frame.sort_values(by="date", ascending=False)
        newest = (newest.drop("year", axis=1)).reset_index(drop=True)

        newest_programs_json = json.loads(newest.to_json(orient="split"))
        del newest_programs_json["index"]

        CollegeMetricsDataStore.save(
            college_metrics=CollegeMetrics(
                date=datetime.now().isoformat(),
                college=College.DAWSON_COLLEGE.name,
                total_programs_offered=total_programs_offered,
                number_of_programs=number_of_programs,
                number_of_profiles=number_of_profiles,
                number_of_disciplines=number_of_disciplines,
                number_of_special_studies=number_of_special_studies,
                number_of_general_studies=number_of_general_education,
                total_year_counts=total_year_counts,
                programs=json.dumps(newest_programs_json),
                number_of_students=number_of_students,
                number_of_faculty=number_of_faculty,
            )
        )
