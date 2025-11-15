from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, url:str, source:str):
        super().__init__()
        self.fetched_url=url
        self.source=source
        
    @abstractmethod
    def scrapeJobs(self):
        pass