import csv
from csv import DictWriter
from dataclasses import dataclass
from typing import List
import requests as req
from bs4 import BeautifulSoup as bs
from bs4.element import ResultSet
from tqdm import tqdm


@dataclass
class CompanyInfo:
    job_title: str
    company: str
    lump_sum_per_month: int
    incentive: str
    duration_in_days: int
    location: str
    apply_by: str
    applicants: int
    number_of_openings: int
    skill_set: list[str]
    perks: list[str]
    src_url: str


class ScrapInternshala:
    def __init__(self):
        self._base_url = "https://internshala.com"
        _python_intern_page = "internships/keywords-python"
        self._python_internship_page_url = ["{}/{}/page-{}".format(self._base_url, _python_intern_page, i) for i in
                                            range(1, 3)]
        self._company_info_list = []  # type: List[CompanyInfo]

    def scrap_all_pages(self) -> None:
        for url in self._python_internship_page_url:
            self._scrap_url(url)

    def dump(self, file_path: str) -> None:
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["job_title", "company", "lump_sum_per_month", "incentive",
                                                   "duration_in_days", "location", "apply_by", "applicants",
                                                   "number_of_openings", "skill_set", "perks", "src_url", ])
            writer.writeheader()
            self._write_file(writer)

    def _write_file(self, writer: DictWriter) -> None:
        for ele in tqdm(self._company_info_list, desc="Dumping..."):
            writer.writerow(
                {"job_title": ele.job_title,
                 "company": ele.company,
                 "lump_sum_per_month": ele.lump_sum_per_month,
                 "incentive": ele.incentive,
                 "duration_in_days": ele.duration_in_days,
                 "location": ele.location,
                 "apply_by": ele.apply_by,
                 "applicants": ele.applicants,
                 "number_of_openings": ele.number_of_openings,
                 "skill_set": ele.skill_set,
                 "perks": ele.perks,
                 "src_url": ele.src_url})

    def _scrap_url(self, url: str) -> None:
        page_src = req.get(url).text
        page_soup = bs(page_src, "html.parser")
        companies_box = page_soup.findAll("a", {"class": "view_detail_button"})

        for company in tqdm(companies_box, desc="Scrapping companies..."):
            details_url = self._base_url + company["href"]
            company_details_src = req.get(details_url).text
            company_details_soup = bs(company_details_src, "html.parser")
            company_info = self._parse_company_info(company_details_soup, details_url)
            self._company_info_list.append(company_info)

    @classmethod
    def _parse_company_info(cls, company_soup: bs, detail_url: str) -> CompanyInfo:
        job_title = company_soup.find("span", {"class": "profile_on_detail_page"}).text.strip()
        company = company_soup.find("a", {"class": "link_display_like_text"}).text.strip()
        stipend = cls._get_stipend(company_soup.find("span", {"class": "stipend"}).text)
        incentive = cls._get_incentive(company_soup.findAll("i"))
        duration_in_days = cls._get_duration(company_soup.findAll("div", {"class": "item_body"}))
        location = company_soup.find("a", {"class": "location_link"}).text.strip()
        apply_by = cls._get_apply_by(company_soup.findAll("div", {"class": "item_body"}))
        applicants = cls._get_applicants(company_soup.find("div", {"class": "applications_message"}).text.strip())
        number_of_openings = cls._get_number_of_openings(company_soup.findAll("div", {"class": "text-container"}))
        skill_set = cls._get_skills_set(company_soup)
        perks = cls._get_perks(company_soup)
        src_url = detail_url

        return CompanyInfo(job_title, company, stipend, incentive, duration_in_days, location, apply_by, applicants,
                           number_of_openings, skill_set, perks, src_url)

    @staticmethod
    def _get_applicants(raw_text: str) -> int:
        applicants = raw_text.split()
        if len(applicants) == 2:
            return int(applicants[0])
        return 0

    @staticmethod
    def _get_perks(company_soup: bs) -> list[str]:
        perks = []
        perks_result_set = company_soup.findAll("div", {"class": "section_heading heading_5_5"})
        for heading in perks_result_set:
            if "Perks" in heading.text:
                children = heading.find_next("div", {"class": "round_tabs_container"}).children
                for perk in children:
                    if perk != "\n":
                        perks.append(perk.text)
                return perks
        return ["Not mentioned"]

    @staticmethod
    def _get_skills_set(company_soup: bs) -> list[str]:
        skill_set = []
        skill_result_set = company_soup.findAll("div", {"class": "section_heading heading_5_5"})
        for heading in skill_result_set:
            if "Skill(s) required" in heading.text:
                children = heading.find_next("div", {"class": "round_tabs_container"}).children
                for skill in children:
                    if skill != "\n":
                        skill_set.append(skill.text)
                return skill_set
        return [""]

    @staticmethod
    def _get_number_of_openings(company_soup: ResultSet) -> int:
        for i in company_soup:
            try:
                if type(int(i.text)) is int:
                    return int(i.text)
            except:
                pass

    @staticmethod
    def _get_apply_by(company_soup: ResultSet) -> str:
        for apply in company_soup:
            if "'" in apply.text:
                return apply.text.strip()

    @staticmethod
    def _get_incentive(company_soup: ResultSet) -> str:
        incentive = "0"
        for i in company_soup:
            try:
                text = i.get("popover_content")
                if "starting" in text:
                    continue
                elif "%" in text:
                    idx = text.index("(")
                    incentive = text[idx + 1:-2]
                else:
                    idx = text.index("(")
                    incentive = text[idx + 3:-2]
            except:
                pass
        return incentive

    @staticmethod
    def _get_stipend(raw_text: str) -> int:
        salary = "".join(raw_text.lstrip().split(" /month"))
        if len(salary) < 6:
            return int(salary)
        elif len(salary) > 5:
            if "-" in raw_text and " lump sum" in raw_text:
                raw_salary = raw_text.split(" lump sum")
                raw_salary = raw_salary[0].split("-")
                avg = (int(raw_salary[0]) + int(raw_salary[1])) // 2
                return int(avg)
            elif "-" in salary:
                salary = list(map(int, salary.split("-")))
                avg = (salary[0] + salary[1]) // 2
                return int(avg)
            elif " lump sum +  Incentives" in salary:
                salary = "".join(salary.split(" lump sum +  Incentives"))
                return int(salary)
            elif " +  Incentives" in salary:
                salary = "".join(salary.split(" +  Incentives"))
                return int(salary)
            elif " lump sum" in salary:
                salary = "".join(salary.split(" lump sum"))
                return int(salary)
            else:
                salary = 0
                return salary

    @staticmethod
    def _get_duration(company_result_set: ResultSet) -> int:
        for duration in company_result_set:
            if "Months" in duration.text or "Month" in duration.text:
                duration = duration.text.split()
                return int(duration[0]) * 30


if __name__ == "__main__":
    scrapper = ScrapInternshala()
    scrapper.scrap_all_pages()
    scrapper.dump(r"C:\Users\DELL\Desktop\scrap_for_python\only_python_scrap.csv")
