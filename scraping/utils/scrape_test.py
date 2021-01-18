# import scraping.utils.indeed_scrape as indeed_scrape
import indeed_scrape

def scrape() -> int:
    scraper = indeed_scrape.IndeedScraper()
    soup = scraper.search(
        what='software engineering', city='Austin', state='Texas'
        )
    print(soup.prettify())
    print('hi')
    return 0



if __name__ == "__main__":
    scrape()
