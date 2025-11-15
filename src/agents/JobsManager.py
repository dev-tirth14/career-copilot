from ..tools.LinkedInScraper import LinkedInScraper
from ..database.models import DatabaseManager
from ..utils.config import Config
from datetime import datetime
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
import time
import yaml, json

class JobsManager:
    def __init__(self):
        self.scrapers=[LinkedInScraper()]
        self.db_manager=DatabaseManager()
        self.llm = Ollama(model="llama3.2")

        prompts_file=Config.PROMPT_DIR.joinpath("JobManager.yaml")
        if(not prompts_file.exists()):
            raise Exception("JobManager prompt file foes not exist")
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)

    def scrape_all_jobs(self):
        for scraper in self.scrapers:
            jobs=scraper.scrapeJobs()
            for job in jobs:
                if(self.db_manager.does_job_exist(job_id=job.get("job_id"))):
                    continue
                # MAKE LLM CALL TO PARSE JOB DETAILS FOR DESCRIPTION AND REQUIREMENTS
                self._llm_parse_job(job=job)
                # BUILD AND SAVE JOB POSTING
                self.db_manager.add_job_posting(job_details=job)
    
    def get_scraped_jobs(self):
        jobs=self.db_manager.get_all_jobs()
        for job in jobs:
            print(f"-----------{job.job_id}-----------")
            print(f"----------------------------------")
            print(job.title)
            print(job.company)
            print(job.description)
            print(job.requirements)
            print(job.key_technologies)
            print(job.processed)
            print()
            print()
    
    def _parse_and_save_job(self, job: dict[str,str|int]):
        if(self.db_manager.does_job_exist(job_id=job.get("job_id"))):
            return
        
    def _llm_parse_job(self,job:dict[str,str|int]) -> dict[str,str]:
        job_details=job.get("role_details")
        if(not job_details):
            raise Exception(f"EMPTY JOB DETAILS FOR JOB: {job.get("job_id")}")
        
        prompt=PromptTemplate.from_template(self.prompts.get("job_extraction")).format(job_content=job_details)
        start_time = time.perf_counter()
        try:
            resp=self.llm.invoke(prompt)
            print(resp)
            resp_obj=json.loads(resp)
            for key in ["description", "requirements","key_technologies"]:
                if (key not in resp_obj):
                    raise(Exception("INVALID LLM RESPONSE"))
        except Exception as e:
            print("LLM Inference ERROR")
            raise Exception(e)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        job.update(resp_obj)

        # Print the duration in seconds
        print(f"The operation took {elapsed_time:.4f} seconds.")
        

        