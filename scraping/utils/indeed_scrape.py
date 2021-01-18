import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import django

class IndeedScraper:
    """
    For each job description that the scraper comes across,  
    """
    def __init__(self) -> None:
        # super().__init__()
        'https://www.indeed.com/jobs?q=software+engineer&l=Seattle%2C+WA'

        self.base_url = 'https://www.indeed.com/'
        return
    
    def search(self, what: str, city: str, state: str, by_date=True) -> BeautifulSoup:
        """gets first page of the search"""
        search_url = self.base_url + 'jobs?q='
        for word in what.split(' '):
            search_url += word + '+'
        search_url = search_url[:len(search_url)-1]
        search_url += '&l=' + city + '%2C+' + state
        
        search_page = requests.get(search_url)
        search_soup = BeautifulSoup(
            search_page.content, 'lxml'
            )
        return search_soup