import csv
from csv import DictWriter
from dataclasses import dataclass
from typing import List, Optional
import requests as req
from bs4 import BeautifulSoup as bs
from bs4.element import ResultSet
from datetime import date
from tqdm import tqdm
import logging
from src.get_stipend import GetStipend


class AttemptsHandler:
    def __init__(self, max_attempts: int):
        self._max_attempts = max_attempts
        self._cur_attempt = 0

    def increment_cur_attempt(self) -> None:
        self._cur_attempt += 1

    def is_attempts_left(self) -> bool:
        return self._cur_attempt < self._max_attempts


@dataclass
class CompanyInfo:
    internship_id: str
    job_title: str
    company: str
    monthly_lump_sum: int
    weekly_lump_sum: int
    incentive: str
    duration_in_days: int
    location: str
    apply_by: date
    applicants: int
    number_of_openings: int
    skill_set: List[str]
    perks: List[str]
    src_url: str


class ScrapInternshala:
    def __init__(self, keyword_search: str):
        self._base_url = "https://internshala.com"
        _python_intern_page = "internships/keywords-{}".format(keyword_search)
        _total_pages = self._get_total_pages("{}/{}/page-1".format(self._base_url, _python_intern_page))
        self._python_internship_page_url = ["{}/{}/page-{}".format(self._base_url, _python_intern_page, i) for i in
                                            range(1, _total_pages + 1)]
        self._company_info_list = []  # type: List[CompanyInfo]

    def scrap_all_pages(self) -> None:
        page_no = 1
        for url in self._python_internship_page_url:
            self._scrap_url(url, page_no)
            page_no += 1

    def dump(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["internship_id", "job_title", "company", "monthly_lump_sum",
                                                   "weekly_lump_sum",
                                                   "incentive", "duration_in_days", "location", "apply_by",
                                                   "applicants", "number_of_openings", "skill_set", "perks",
                                                   "src_url", ])
            writer.writeheader()
            self._write_file(writer)

    @staticmethod
    def _get_total_pages(url: str) -> int:
        page_src = req.get(url).text
        page_soup = bs(page_src, "html.parser")
        return int(page_soup.find("span", {"id": "total_pages"}).text)

    def _write_file(self, writer: DictWriter) -> None:
        for ele in tqdm(self._company_info_list, desc="Dumping..."):
            writer.writerow(
                {"internship_id": ele.internship_id,
                 "job_title": ele.job_title,
                 "company": ele.company,
                 "monthly_lump_sum": ele.monthly_lump_sum,
                 "weekly_lump_sum": ele.weekly_lump_sum,
                 "incentive": ele.incentive,
                 "duration_in_days": ele.duration_in_days,
                 "location": ele.location,
                 "apply_by": ele.apply_by,
                 "applicants": ele.applicants,
                 "number_of_openings": ele.number_of_openings,
                 "skill_set": ele.skill_set,
                 "perks": ele.perks,
                 "src_url": ele.src_url
                 }
            )

    def _scrap_url(self, url: str, page_no: int) -> None:
        page_src = req.get(url).text
        page_soup = bs(page_src, "html.parser")
        companies_box = page_soup.findAll("div", {"class": "heading_4_5 profile"})

        for company in tqdm(companies_box, desc="Scrapping page {} companies.".format(page_no)):
            details_url = self._base_url + company.a.get("href")
            company_details_src = req.get(details_url).text
            company_details_soup = bs(company_details_src, "html.parser")
            company_info = self._parse_company_info(company_details_soup, details_url)
            self._company_info_list.append(company_info)

    @classmethod
    def _parse_company_info(cls, company_soup: bs, detail_url: str) -> CompanyInfo:
        internship_id = cls._get_internship_id(company_soup)
        job_title = company_soup.find("span", {"class": "profile_on_detail_page"}).text.strip()
        company = company_soup.find("a", {"class": "link_display_like_text"}).text.strip()
        m_stipend, w_stipend = GetStipend.get_stipend(company_soup.find("span", {"class": "stipend"}).text)
        incentive = cls._get_incentive(company_soup.findAll("i"))
        duration_in_days = cls._get_duration(company_soup.findAll("div", {"class": "item_body"}))
        location = company_soup.find("a", {"class": "location_link"}).text.strip()
        apply_by = cls._get_apply_by(company_soup)
        applicants = cls._get_applicants(company_soup.find("div", {"class": "applications_message"}).text.strip())
        number_of_openings = cls._get_number_of_openings(company_soup.findAll("div", {"class": "text-container"}))
        skill_set = cls._get_skills_set(company_soup)
        perks = cls._get_perks(company_soup)
        src_url = detail_url

        return CompanyInfo(internship_id, job_title, company, m_stipend, w_stipend, incentive, duration_in_days,
                           location, apply_by, applicants, number_of_openings, skill_set, perks, src_url)

    @staticmethod
    def _get_internship_id(company_soup: bs) -> str:
        return company_soup.find("div", {"class": "detail_view"}).div.attrs["internshipid"]

    @staticmethod
    def _get_applicants(raw_text: str) -> int:
        if "+" in raw_text:
            applicants = raw_text.split("+ ")
            return int(applicants[0])
        else:
            logging.info(raw_text)
        applicants = raw_text.split()
        if len(applicants) == 2:
            return int(applicants[0])
        else:
            logging.info(applicants)
        return 0

    @staticmethod
    def _get_perks(company_soup: bs) -> List[str]:
        perks = []
        perks_result_set = company_soup.findAll("div", {"class": "section_heading heading_5_5"})
        for heading in perks_result_set:
            if "Perks" in heading.text:
                children = heading.find_next("div", {"class": "round_tabs_container"}).children
                for perk in children:
                    if perk != "\n":
                        perks.append(perk.text)
                    else:
                        logging.info(perk)
                return perks
            else:
                logging.info(heading.text)
        return [""]

    @staticmethod
    def _get_skills_set(company_soup: bs) -> List[str]:
        skill_set = []
        skill_result_set = company_soup.findAll("div", {"class": "section_heading heading_5_5"})
        for heading in skill_result_set:
            if "Skill(s) required" in heading.text:
                children = heading.find_next("div", {"class": "round_tabs_container"}).children
                for skill in children:
                    if skill != "\n":
                        skill_set.append(skill.text)
                    else:
                        logging.info(skill)
                return skill_set
            else:
                logging.info(heading.text)

        return [""]

    @staticmethod
    def _get_number_of_openings(company_soup: ResultSet) -> int:
        for i in company_soup:
            if i.text.strip().isdigit():
                return int(i.text)
            else:
                logging.info(i.text)

    @staticmethod
    def _get_apply_by(company_soup: bs) -> Optional[date]:
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
                  "Nov": 11, "Dec": 12}
        res = company_soup.find("div", {
            "class": ["other_detail_item apply_by", "other_detail_item large_stipend_text apply_by"]}).find("div", {
            "class": "item_body"}).text
        if res == "Not Provided":
            return None
        final = res.replace("'", "").split()
        d = date(date.today().year, months[final[1]], int(final[0]))
        return d

    @staticmethod
    def _get_incentive(company_soup: ResultSet) -> str:
        incentive = "0"

        for i in company_soup:
            text = i.get("popover_content")
            if text is None:
                continue
            elif "starting" in text:
                continue
            elif "%" in text:
                idx = text.index("(")
                incentive = text[idx + 1:-2]
            elif "%" not in text:
                idx = text.index("(")
                incentive = text[idx + 3:-2]
            else:
                logging.info(text)
        return incentive

    @staticmethod
    def _get_duration(company_result_set: ResultSet) -> int:
        for duration in company_result_set:
            if "Months" in duration.text or "Month" in duration.text:
                duration = duration.text.split()
                return int(duration[0]) * 30
            elif "Weeks" in duration.text or "Week" in duration.text:
                duration = duration.text.split()
                return int(duration[0]) * 7
            else:
                logging.info(duration.text.strip())
