from .base import BaseScraper
from ..config.settings import Config
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
import time
import requests
from datetime import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class LinkedInScraper(BaseScraper):
    def __init__(self):
        super().__init__(url=Config.SCRAPER_URLs.get("LinkedIn"), source="LinkedIn")
    
    def scrapeJobs(self):
        jobs=[]
        start_index=0
        while True:
            if(start_index>0):
                break
            url_to_fetch=self.fetched_url.format(start_index=start_index)
            response=requests.get(url=url_to_fetch)
            soup=BeautifulSoup(response.content,"html.parser")
            job_cards=soup.find_all(class_="base-card")
            if(len(job_cards)==0):
                break
            else:
                start_index=start_index+len(job_cards)
            
            for index in range(len(job_cards)):
                job_card=job_cards[index].find(class_="base-card__full-link")
                job_url=job_card.attrs.get("href")
                job_id=job_cards[index].attrs.get("data-entity-urn").split(":")[-1]
                try:
                    response=requests.get(url=job_url, headers=headers)
                    time.sleep(1)
                except Exception as e:
                    print(f"FAILED TO RETRIEVE: {job_url}",e)
                    continue
                jobSoup=BeautifulSoup(response.content, "html.parser")
                company=jobSoup.find(class_="topcard__org-name-link")
                role=jobSoup.find(class_="top-card-layout__title")
                job_location=jobSoup.find(class_="aside-job-card__location")
                raw_role_details=jobSoup.find(class_="show-more-less-html__markup")
                try:
                    job={
                        "job_id":job_id,
                        "company":company.text.strip(),
                        "title":role.text.strip(),
                        "location":job_location.text.strip(),
                        "role_details":raw_role_details.get_text('\n').strip(),
                        "url":f"https://www.linkedin.com/jobs/view/{job_id}",
                        "source":self.source,
                        "scraped_at":datetime.now()
                    }
                    jobs.append(job)
                    print(f"Scrape Successful for job: {job["job_id"]}")
                except Exception as e:
                    print(f"Scrape FAILED for job {job_url} because: {e}")
                    continue
        return jobs

            