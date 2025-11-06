from threading import Thread
import heapq
from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time
import report

class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def run(self):
        count = 0
        while True:
            count += 1
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)

            if count % 500 == 0:
                self.logger.info(f"Reached {count} pages — generating intermediate report...")
                report.generate_report(full=False)
            
        self.logger.info("Generating final report...")
        report.generate_report(full=True)
        self.logger.info("Report generated successfully as 'report2.txt'.")

    def find_top_fifty(self, total_freqs):
        return heapq.nlargest(50, total_freqs.items(), key=lambda x: x[1])
