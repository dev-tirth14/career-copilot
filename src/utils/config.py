from pathlib import Path

# Manages paths and settings
class Config:
    PROJECT_ROOT_DIR=Path(__file__).parent.parent.parent
    DATA_DIR=PROJECT_ROOT_DIR.joinpath("data")
    PROMPT_DIR=PROJECT_ROOT_DIR.joinpath("src","prompts")
    SCRAPER_URLs={
        "LinkedIn":"https://linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=AI&location=Greater%20Toronto%20Area,%20Canada&f_TPR=r84600&start={start_index}"
    }