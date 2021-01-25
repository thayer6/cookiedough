import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
import django

# load class from models
from scraping.models import Job
from scraping.utils import indeed_scrape


class Command(BaseCommand):
    help = "collect jobs"

    # define logic of command -- tells django it is an admin command

    def handle(self, *args, **options) -> None:
        #TODO create an input for the command to pass a list of jobs to update
        """
        but that needs to be discussed. it may be better just to have a 
        list to run through with and update
        """
        jobs = ['software engineer', 
        'machine learning engineer', 
        'data scientist'
        ]
        places = [{'city': 'Austin', 'state': 'Texas'}, 
        {'city': 'Seattle', 'state': 'Washington'}]
        num_pages = 3
        scraper = indeed_scrape.IndeedScraper(
            jobs=jobs, locations=places, num_pages=num_pages
        )
        scraper.large_search()

        return 

