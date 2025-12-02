"""
Career Copilot - AI-powered job matching system
Main entry point for the application
"""

from .services.resume_service import ResumeManager
from .services.job_service import JobsManager
from .core.matching.agent import MatchingAgent
from .config.settings import Config
from pathlib import Path


def main():
    """Main application entry point"""

    # Initialize services
    # resume_manager = ResumeManager()
    job_manager = JobsManager()
    # jobs=job_manager.get_scraped_jobs()
    # for job in jobs:
    #     print(job.url)
    #     print(job.description)
    #     print(job.key_technologies)
    #     print(job.requirements)
        # print("-"*40)
    # resume_manager.process_resume(file_path=Config.DATA_DIR.joinpath("resumes", "resume_2025.pdf"))
    job_manager.scrape_all_jobs()

    matcher = MatchingAgent()

    # Get active resume
    # Uncomment to process a new resume:
    # from .config.settings import Config
    # resume_manager.process_resume(Config.DATA_DIR.joinpath("resumes", "resume_2025.pdf"))

    # Scrape and process jobs
    # Uncomment to scrape new jobs:
    # job_manager.scrape_all_jobs()

    # Match jobs with resume
    # results = matcher.match_all_jobs()



if __name__ == "__main__":
    main()
