# Career Copilot

An AI-powered job matching system that uses RAG (Retrieval-Augmented Generation) to intelligently match your resume with job postings.

## Features

- **Resume Parsing**: Extract structured data from PDF resumes
- **Job Scraping**: Automatically scrape job postings from LinkedIn and other sources
- **Intelligent Matching**: RAG-powered matching system with skill context enrichment
- **Knowledge Base**: Vector database of technical skills, tools, and manifestations
- **Scoring System**: Detailed scoring across technical skills, experience, education, and role alignment

## Project Structure

```
career-copilot/
├── src/
│   ├── core/                    # Core business logic
│   │   ├── matching/            # Job matching logic
│   │   │   ├── agent.py         # MatchingAgent
│   │   │   └── context_builder.py
│   │   └── knowledge/           # RAG knowledge system
│   │       └── store.py         # KnowledgeStore (vector DB)
│   │
│   ├── services/                # Application services
│   │   ├── resume_service.py    # Resume management
│   │   └── job_service.py       # Job scraping & management
│   │
│   ├── scrapers/                # Web scrapers
│   │   ├── base.py              # BaseScraper
│   │   └── linkedin.py          # LinkedInScraper
│   │
│   ├── parsers/                 # Document parsers
│   │   └── resume.py            # ResumeParser
│   │
│   ├── models/                  # Database models
│   │   ├── entities.py          # Resume & Job entities
│   │   └── database.py          # DatabaseManager
│   │
│   ├── prompts/                 # LLM prompts
│   │   ├── matching.yaml
│   │   ├── resume.yaml
│   │   └── job.yaml
│   │
│   ├── config/                  # Configuration
│   │   └── settings.py
│   │
│   └── main.py                  # Entry point
│
├── data/                        # Data storage
│   ├── database.db              # SQLite database
│   ├── resumes/                 # Resume PDFs
│   ├── knowledge/               # Knowledge base files
│   └── vector_db/               # ChromaDB vector store
│
├── tests/                       # Unit tests
├── logs/                        # Application logs
└── requirements.txt             # Dependencies
```

## Setup

### Quick Start with UV (Recommended)

This project uses **UV** for fast, modern Python dependency management.

1. **Install UV**:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or with Homebrew
   brew install uv
   ```

2. **Setup project**:
   ```bash
   # Create virtual environment
   uv venv

   # Activate it
   source .venv/bin/activate

   # Install all dependencies (10-100x faster than pip!)
   uv sync
   ```

3. **Set up Ollama** (for local LLM):
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.2
   ```

4. **Prepare knowledge base**:
   - Add skill definitions to `data/knowledge/skills/`
   - Run knowledge processing to populate vector DB

5. **Add resume**:
   - Place PDF resume in `data/resumes/`
   - Process with ResumeManager

See [SETUP.md](SETUP.md) for detailed setup instructions and UV command reference.

### Alternative: Traditional Setup

If you prefer pip:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from src.main import main

# Run full pipeline
results = main()
```

### Process New Resume

```python
from src.services.resume_service import ResumeManager
from src.config.settings import Config

resume_manager = ResumeManager()
resume_manager.process_resume(Config.DATA_DIR.joinpath("resumes", "your_resume.pdf"))
```

### Scrape Jobs

```python
from src.services.job_service import JobsManager

job_manager = JobsManager()
job_manager.scrape_all_jobs()
```

### Match Jobs

```python
from src.core.matching.agent import MatchingAgent

matcher = MatchingAgent()
results = matcher.match_all_jobs()

# Results are sorted by recommendation (STRONG > GOOD > MODERATE > WEAK > POOR)
for result in results:
    job = result['job']
    match = result['match']
    print(f"{job.title} at {job.company}: {match['total_score']}/100")
```

## How It Works

### 1. Resume Processing
- Extracts text from PDF
- Uses LLM to parse structured data (skills, experience, education)
- Stores in SQLite database

### 2. Job Scraping
- Scrapes job postings from configured sources
- Extracts requirements and technologies using LLM
- Stores in database

### 3. RAG-Enhanced Matching
- **Context Building**: For each job-resume pair:
  - Identifies all relevant skills from both job and resume
  - Queries vector database for:
    - Skill definitions
    - Related tools/technologies
    - Real-world manifestations
- **Scoring**: LLM evaluates match across:
  - Technical Skills (40 pts)
  - Experience Level (25 pts)
  - Education (15 pts)
  - Role Alignment (20 pts)
- **Recommendation**: STRONG/GOOD/MODERATE/WEAK/POOR MATCH

### 4. Knowledge Store (RAG)
- Vector database (ChromaDB) storing:
  - **Definitions**: What each skill/technology means
  - **Tools**: Related frameworks, libraries, platforms
  - **Manifestations**: How skills appear in real work experience
- Enables semantic matching beyond keyword matching

## Configuration

Edit `src/config/settings.py` to configure:
- Data directories
- Scraper URLs
- Knowledge base settings
- Vector DB parameters

## Dependencies

- **LLM**: Ollama (llama3.2)
- **Vector DB**: ChromaDB
- **Database**: SQLite (SQLAlchemy)
- **LLM Framework**: LangChain
- **Parsing**: PyPDF2, BeautifulSoup4

## License

MIT License

## Future Enhancements

- [ ] Support for more job sources (Indeed, Glassdoor, etc.)
- [ ] Web UI for results visualization
- [ ] Resume optimization suggestions
- [ ] Cover letter generation
- [ ] Application tracking
- [ ] Email notifications for new matches
