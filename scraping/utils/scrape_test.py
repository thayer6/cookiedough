# import indeed_scrape

import sys
print(sys.path)

from scraping.utils import indeed_scrape

"""this has been moved to commands/scrape.py under handle"""

def scrape() -> int:
    scraper = indeed_scrape.IndeedScraper()
    soup = scraper.search(
        what='software engineering', city='Austin', state='Texas'
        )

    temp_url = scraper.make_search_url(
        job='software engineering', city='Austin', state='Texas'
    )
    job_pull = scraper.job_data_pull(temp_url)
    
    scraper.push_to_database(job_pull=job_pull)
    
    print('task finished')
    return 0



if __name__ == "__main__":
    scrape()
