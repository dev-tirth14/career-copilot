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
    """Simple end-to-end workflow for Career Copilot"""

    print("=" * 60)
    print("Career Copilot - AI-Powered Job Matching")
    print("=" * 60)

    # Step 1: Process resume
    print("\n[1/3] Processing resume...")
    resume_manager = ResumeManager()
    resume_path = Config.DATA_DIR.joinpath("resumes", "resume_2025.pdf")
    resume_manager.process_resume(file_path=resume_path)
    print("✓ Resume processed and stored")

    # Step 2: Scrape jobs
    print("\n[2/3] Scraping jobs from configured sources...")
    job_manager = JobsManager()
    job_manager.scrape_all_jobs()
    print("✓ Jobs scraped and stored")

    # Step 3: Match jobs with resume
    print("\n[3/3] Matching jobs with your resume...")
    matcher = MatchingAgent()
    matcher.match_all_jobs()
    print("✓ Job matching complete")

    print("\n" + "=" * 60)
    print("Workflow complete! Check the database for results.")
    print("=" * 60)



if __name__ == "__main__":
    main()
