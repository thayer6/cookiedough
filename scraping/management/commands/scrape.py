import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm

# load class from models
from scraping.models import Job


class Command(BaseCommand):
    help = "collect jobs"

    # define logic of command -- tells django it is an admin command
    def handle(self, *args, **options):

        # scrape code
        url = "https://www.indeed.com/jobs?q=software+engineer&l=Seattle%2C+WA"

        def job_data_pull(url):
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

        answer = job_data_pull(url)

        for index, a in tqdm(enumerate(answer)):
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
            job_text = str(content.find("div", class_="jobsearch-jobDescriptionText"))

        # check if url in db
        # figure out how to check if it exists and skip!!
        try:
            # save in db
            Job.objects.create(
                job_id=job_id,
                title=title,
                company=company,
                job_url=job_url,
                job_text=job_text,
            )
            print("%s added" % (title,))
        except Job.exists():
            print("%s already exists" % (title,))

        self.stdout.write("job complete")
