import re

import django
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scraping.models import Job

# from ..models import Job


class IndeedScraper:
    """
    For each job description that the scraper comes across,
    """

    def __init__(self, jobs=[], locations=[], num_pages=1) -> None:
        # super().__init__()
        "https://www.indeed.com/jobs?q=software+engineer&l=Seattle%2C+WA"

        self.base_url = "https://www.indeed.com/"
        self.job_list = jobs
        self.locations = locations
        # need to have a function to check that self.locations is the right format

        # this might be changed later
        self.num_pages = num_pages
        return

    # May be irrelevant with Ben's structure
    def search(self, what: str, city: str, state: str, by_date=True) -> BeautifulSoup:
        """gets first page of the search"""
        search_url = self.base_url + "jobs?q="
        for word in what.split(" "):
            search_url += word + "+"
        search_url = search_url[: len(search_url) - 1]
        search_url += "&l=" + city + "%2C+" + state

        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(search_page.content, "lxml")
        return search_soup

    # for understanding job_data_pull
    def make_search_url(
        self, job: str, city: str, state: str, by_date=True, page_num=0
    ) -> str:
        """
        creates url for indeed search page
        """
        search_url = self.base_url + "jobs?q="
        for word in job.split(" "):
            search_url += word + "+"
        search_url = search_url[: len(search_url) - 1]
        search_url += "&l=" + city + "%2C+" + state
        if by_date:
            search_url += "&sort=date"
        if page_num > 0:
            num = 10 * page_num
            search_url += "&start=%i" % num
        return search_url

    @staticmethod
    def job_data_pull(url: str) -> list[dict]:
        """
        Returns a list of dictionaries that contain links to job description
        pages and base information, which can then be passed to the database
        """
        page = requests.get(url)  # go to the page noted by the url
        page_contents = BeautifulSoup(
            page.content, "lxml"
        )  # extract the contents of the page

        # only getting the tags for organic job postings and not the ones that are sponsored
        tags = page_contents.find_all("div", {"data-tn-component": "organicJob"})

        # getting the list of companies that have the organic job posting tags
        companies = [x.span.text for x in tags]

        # extracting the features like the company name, complete link, date, etc.
        attributes = [x.h2.a.attrs for x in tags]
        dates = [x.find_all("span", {"class": "date"}) for x in tags]

        # update attributes dictionaries with company name and date posted
        [
            attributes[i].update({"company": companies[i].strip()})
            for i, x in enumerate(attributes)
        ]
        [
            attributes[i].update({"date posted": dates[i][0].text.strip()})
            for i, x in enumerate(attributes)
        ]
        return attributes

    @staticmethod
    def clean_the_text(text: str, remove_numbers=False) -> str:
        text = text.replace("- ", "")
        text = text.replace("<div>", "    ")
        text = text.replace("</div>", " ")
        text = text.replace("<ul>", "     ")
        text = text.replace("</ul>", " ")
        text = text.replace("<li>", "    ")
        text = text.replace("</li>", " ")
        text = text.replace("<p>", "    ")
        text = text.replace("</p>", " ")
        text = text.replace("<b>", "    ")
        text = text.replace("</b>", " ")
        text = text.replace("<br>", "    ")
        text = text.replace("</br>", " ")
        text = text.replace("<br/>", " ")
        text = text.replace('<h2 class="jobSectionHeader">', " ")
        text = text.replace("</h2>", " ")
        text = text.replace("<i>", "    ")
        text = text.replace("</i>", " ")
        text = text.replace(
            "< =jobsearch-jobDescriptionText id=jobDescriptionText>", ""
        )
        text = text.replace(
            '< ="jobsearch-jobDescriptionText" id="jobDescriptionText">', ""
        )

        return text

    def push_to_database(self, job_pull: list[dict]) -> None:

        for index, a in tqdm(enumerate(job_pull)):
            job_url = a["id"].replace("jl_", "https://www.indeed.com/viewjob?jk=")
            title = a["title"]
            job_id = a["id"]

            page = requests.get(job_url)
            content = BeautifulSoup(page.content, "html.parser")
            companyName = content.find(
                "div", class_="icl-u-lg-mr--sm icl-u-xs-mr--xs", text=True
            )
            company = re.sub("<[^>]+>", "", str(companyName))
            company = company.replace(" &amp; ", " & ")
            job_raw_text = str(
                content.find("div", class_="jobsearch-jobDescriptionText")
            )
            job_clean_text = self.clean_the_text(job_raw_text)

            try:
                # save in db
                Job.objects.create(
                    job_id=job_id,
                    title=title,
                    company=company,
                    job_url=job_url,
                    job_raw_text=job_raw_text,
                    job_clean_text=job_clean_text,
                )
                print("%s added" % (title,))

            except django.db.utils.IntegrityError:
                print("%s already exists" % (title,))

        return

    @staticmethod
    def basic_run():
        """
        An initial testing function to run the basics of my scraper.
        To be deleted later.
        """

        scraper = IndeedScraper()
        temp_url = scraper.make_search_url(
            job="software engineering", city="Austin", state="Texas"
        )
        job_pull = scraper.job_data_pull(temp_url)
        scraper.push_to_database(job_pull=job_pull)
        print("task finished")

        return

    def large_search(self):
        # scraper = IndeedScraper()
        for job in self.job_list:
            for place in self.locations:
                for num in range(self.num_pages):
                    temp_url = self.make_search_url(
                        job=job, city=place["city"], state=place["state"], page_num=num
                    )
                    job_pull = self.job_data_pull(url=temp_url)
                    self.push_to_database(job_pull=job_pull)
        print("task finished")
        return
