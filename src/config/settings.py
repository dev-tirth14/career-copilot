from pathlib import Path


class Config:
    """Application configuration and settings."""

    # Project paths
    PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT_DIR.joinpath("data")
    PROMPT_DIR = PROJECT_ROOT_DIR.joinpath("src", "prompts")
    VECTOR_DB_DIR = DATA_DIR.joinpath("vector_db")

    # Scraper configuration
    SCRAPER_URLs = {
        "LinkedIn": "https://linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=AI&location=Greater%20Toronto%20Area,%20Canada&f_TPR=r84600&start={start_index}"
    }

    # Knowledge store configuration
    CHROMADB_PERSISTANCE_PATH = VECTOR_DB_DIR
    KNOWLEDGE_PATH = DATA_DIR.joinpath("knowledge")
    SKILL_KNOWLEDGE_DIR = "skills"
    SKILL_COLLECTION_NAME = "skills"

    # Knowledge retrieval limits
    PER_SKILL_DEFINITIONS = 1
    PER_SKILL_TOOLS = 1
    PER_EXPERIENCE_MANIFESTATIONS = 3
