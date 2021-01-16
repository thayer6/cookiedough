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

        def clean_the_text(text, remove_numbers=False):
            # from bs4 import BeautifulSoup
            # soup = BeautifulSoup(text, 'lxml')

            # from pattern.web import URL, plaintext
            # text = plaintext(str(text), keep=[], linebreaks=2, indentation=False)

            # text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            # text = unicodedata.normalize('NFKD', str(text)).encode('ascii').decode('utf-8')

            #     clean = re.compile(r'^<.*?>}{')
            #     text = re.sub(clean, '', text)
            text = re.sub("x9307.", "", text)
            text = text.replace("\xef\xac\x81", "fi")
            text = text.replace(" .org", ".org")
            text = text.replace("ISSN ", "ISSN")
            text = text.replace("xef", "")
            text = text.replace("x83", "")
            text = text.replace("x98", "\n")
            text = text.replace("x99", "'")
            text = text.replace("xe2", " ")
            text = text.replace("x80", " ")
            text = text.replace("xa2", "*")
            text = text.replace("\\xc3\\xa9", "e")
            text = text.replace("\\xe2\\x80\\x90", " - ")
            text = text.replace("\\xe2\\x80\\x91", "-")
            text = text.replace("\\xe2\\x80\\x92", "-")
            text = text.replace("\\xe2\\x80\\x93", "-")
            text = text.replace("\\xe2\\x80\\x94", "-")
            text = text.replace("\\xe2\\x80\\x98", "'")
            text = text.replace("\\xe2\\x80\\x99", "'")
            text = text.replace("\\xe2\\x80\\x9b", "'")
            text = text.replace("\\xe2\\x80\\x9c", '"')
            text = text.replace("\\xe2\\x80\\x9d", '"')
            text = text.replace("\\xe2\\x80\\x9e", '"')
            text = text.replace("\\xe2\\x80\\x9f", '"')
            text = text.replace("\\xe2\\x80\\xa6", "...")
            text = text.replace("\\xe2\\x81\\xba", "+")
            text = text.replace("\\xe2\\x81\\xbb", "-")
            text = text.replace("\\xe2\\x81\\xbc", "=")
            text = text.replace("\\xe2\\x81\\xbd", "(")
            text = text.replace("\\xe2\\x81\\xbe", ")")
            # text = text.replace("\'", "'")
            text = text.replace("\\n", "\n ")
            text = text.replace("\n\n", "\n  ")
            text = text.replace("\\xc2\\xae", " ")
            # text = text.replace('\n','    ') # new line
            text = text.replace("\t", "     ")
            # text = text.replace("\s", " ")  # space
            text = text.replace("\r\r\r", " ")  # carrage Return
            text = text.replace("\\xc2\\xa9 ", " ")
            text = text.replace("xe2x80x93", ",")
            text = text.replace("xe2x88x92", " ")
            text = text.replace("\\x0c", " ")
            text = text.replace("\\xe2\\x80\\x9331", " ")
            text = text.replace("xe2x80x94", " ")
            text = text.replace("\x0c", " ")
            text = text.replace("]", "] ")
            # text = text.replace(' x99', "'")
            # text = text.replace('xe2x80x99', "'")
            text = text.replace("\\xe2\\x80\\x933", "-")
            text = text.replace("\\xe2\\x80\\x935", "-")
            text = text.replace("\\xef\\x82\\xb7", " ")
            text = text.replace("\\", " ")
            text = text.replace("xe2x80x99", "'")
            text = text.replace("xe2x80x9cwexe2x80x9d", " ")
            text = text.replace("xe2x80x93", ", ")
            text = text.replace("xe2x80x9cEUxe2x80x9d", " ")
            text = text.replace("xe2x80x9cxe2x80x9d", " ")
            text = text.replace("xe2x80x9cAvastxe2x80x9d", " ")
            text = text.replace("xc2xa0", " ")
            text = text.replace("xe2x80x9cxe2x80x9d", " ")
            text = text.replace("xe2x80x9c", " ")
            text = text.replace("xe2x80x9d", " ")
            text = text.replace("xc2xad", " ")
            text = text.replace("x07", " ")
            text = text.replace("tttttt", " ")
            text = text.replace("activetttt.", " ")
            text = text.replace(".sdeUptttt..sdeTogglettttreturn", " ")
            text = text.replace("ttif", " ")
            text = text.replace(".ttt.", " ")
            text = text.replace(" t t ", " ")
            text = text.replace("tttt ", " ")
            text = text.replace(" tt ", " ")
            text = text.replace(" t ", " ")
            text = text.replace(" t tt t", " ")
            text = text.replace("ttt", " ")
            text = text.replace("ttr", " ")
            text = text.replace(".display", " ")
            text = text.replace("div class", " ")
            text = text.replace("div id", " ")
            text = text.replace("Pocy", "Policy")
            text = text.replace("xc2xa0a", " ")
            text = text.replace(" b ", "")
            text = text.replace("rrrr", "")
            text = text.replace("rtttr", "")
            text = text.replace("    ", " ")
            text = text.replace("   ", " ")
            text = text.replace("  ", " ")
            text = text.replace(" r ", " ")
            text = text.replace(" tr ", " ")
            text = text.replace(" rr  r  ", " ")
            text = text.replace("   tt t t rt ", " ")
            text = text.replace("r rrr r trr ", " ")
            text = text.replace(" xe2x80x93 ", " ")
            text = text.replace(" xe6xa8x82xe9xbdxa1xe6x9cx83  ", " ")
            text = text.replace(" rrr ", " ")
            text = text.replace(" rr ", " ")
            text = text.replace("tr ", "")
            text = text.replace(" r ", "")
            text = text.replace("'", "")
            text = text.replace(" t* ", ", ")
            text = text.replace("[pic]", "")
            text = text.replace("    ", "")
            text = text.replace("|", "")
            text = text.replace("__", "")
            text = text.replace('b"', "")
            text = text.replace("xe2x80xa2", ". ")
            text = text.replace("\x0c", "")
            text = text.replace("xc2", "")
            text = text.replace("xa0", "")
            text = text.replace("x99s", "- ")
            text = text.replace("x9d", "")
            text = text.replace("x9c", "")
            text = text.replace(" x93 ", ": ")
            text = text.replace("....", "")
            text = text.replace(" s ", "'s ")
            text = text.replace(" xac x81", " fi")
            text = text.replace("peci fi", "pecifi")
            text = text.replace("xc3 x9f", "copyright")
            text = text.replace(" et al ", "etal")
            text = text.replace("x97 x8f ", "*")
            text = text.replace(" x937 ", ": ")
            text = text.replace(" xac x82", "sp")
            text = text.replace(" x90", "-")
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
            text = text.replace("<i>", "    ")
            text = text.replace("</i>", " ")
            text = text.replace(
                "< =jobsearch-jobDescriptionText id=jobDescriptionText>", ""
            )
            text = text.replace(
                '< ="jobsearch-jobDescriptionText" id="jobDescriptionText">', ""
            )
            # _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
            # text = _RE_COMBINE_WHITESPACE.sub(" ", text).strip()

            return text

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
            job_raw_text = str(
                content.find("div", class_="jobsearch-jobDescriptionText")
            )
            job_clean_text = clean_the_text(job_raw_text)

        # check if url in db
        # figure out how to check if it exists and skip!!
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

        except Job.exists():
            print("%s already exists" % (title,))

        self.stdout.write("job complete!")
