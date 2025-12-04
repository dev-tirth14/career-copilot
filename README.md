# Career Copilot

An AI-powered job matching system that uses RAG (Retrieval-Augmented Generation) to intelligently match your resume with job postings. Built with local LLMs (Ollama) and vector databases (ChromaDB) for privacy-focused, intelligent job matching.

## Features

- **Resume Parsing**: Extract structured data from PDF resumes using LLM-powered parsing
- **Job Scraping**: Automatically scrape job postings from LinkedIn with LLM-based requirement extraction
- **RAG-Enhanced Matching**: Context-aware matching system that enriches job-resume comparisons with skill definitions, related technologies, and real-world manifestations
- **Vector Knowledge Base**: ChromaDB-powered vector database storing semantic information about technical skills, tools, and manifestations
- **Intelligent Scoring**: Multi-dimensional scoring across technical skills (40%), experience (25%), education (15%), and role alignment (20%)

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

## Prerequisites

- **Python 3.10+** (required)
- **Ollama** - For local LLM inference ([download here](https://ollama.ai))
- **UV** - Fast Python package manager (recommended, [install guide](https://docs.astral.sh/uv/))

## Setup

### Quick Start with UV (Recommended)

This project uses **UV** for fast, modern Python dependency management (10-100x faster than pip).

1. **Install UV**:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Or with Homebrew
   brew install uv

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone and setup project**:
   ```bash
   git clone <repository-url>
   cd career-copilot

   # Create virtual environment
   uv venv

   # Activate it
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows

   # Install all dependencies
   uv sync
   ```

3. **Set up Ollama**:
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull the required model (llama3.2)
   ollama pull llama3.2

   # Start Ollama service (runs in background)
   ollama serve
   ```

4. **Prepare data directories** (auto-created on first run):
   ```
   data/
   ├── resumes/          # Place your resume PDFs here
   ├── knowledge/        # Knowledge base files (skills definitions)
   │   └── skills/
   └── vector_db/        # ChromaDB storage (auto-generated)
   ```

5. **Add your resume**:
   ```bash
   # Place your resume in data/resumes/
   cp ~/path/to/resume.pdf data/resumes/
   ```

See [SETUP.md](SETUP.md) for detailed setup instructions and UV command reference.
See [UV_GUIDE.md](UV_GUIDE.md) for UV-specific commands and workflow.

### Alternative: Traditional Setup

If you prefer pip:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the main application
python -m src.main

# Or run directly
python src/main.py
```

### Workflow

The typical workflow is:

1. **Process Resume** → 2. **Scrape Jobs** → 3. **Match Jobs**

The current [src/main.py](src/main.py) runs all three steps automatically:

```python
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
```

**Note**: Update the `resume_path` in [src/main.py:23](src/main.py#L23) to match your resume filename before running

### Individual Components

#### Process a New Resume

```python
from src.services.resume_service import ResumeManager
from src.config.settings import Config

resume_manager = ResumeManager()
resume_manager.process_resume(
    Config.DATA_DIR.joinpath("resumes", "your_resume.pdf")
)
```

This will:
- Extract text from PDF using PyPDF2
- Parse structured data (name, email, skills, experience, education) using LLM
- Store in SQLite database with `is_active=True`

#### Scrape Jobs

```python
from src.services.job_service import JobsManager

job_manager = JobsManager()
job_manager.scrape_all_jobs()  # Scrapes from configured sources

# Get all scraped jobs
jobs = job_manager.get_scraped_jobs()
```

Current sources: LinkedIn (AI jobs in Greater Toronto Area, posted in last 24h)

Configure URLs in [src/config/settings.py](src/config/settings.py#L14-L16)

#### Match Jobs with Resume

```python
from src.core.matching.agent import MatchingAgent

matcher = MatchingAgent()
results = matcher.match_all_jobs()

# Results are sorted by recommendation and score
# STRONG MATCH > GOOD MATCH > MODERATE MATCH > WEAK MATCH > POOR MATCH
for result in results:
    job = result['job']
    match = result['match']
    print(f"{job.title} at {job.company}")
    print(f"Score: {match['total_score']}/100 - {match['recommendation']}")
    print(f"Matching Skills: {match['matching_skills']}")
    print(f"Missing Skills: {match['missing_skills']}")
```

## How It Works

### Architecture Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Resume    │      │  Job Scraper │      │  Knowledge Base │
│   Parser    │──┐   │  (LinkedIn)  │──┐   │   (ChromaDB)    │
└─────────────┘  │   └──────────────┘  │   └─────────────────┘
                 │                     │            │
                 ↓                     ↓            ↓
            ┌────────────────────────────────────────────┐
            │         SQLite Database                    │
            │  ┌──────────┐      ┌──────────────────┐   │
            │  │ Resumes  │      │  Job Postings    │   │
            │  └──────────┘      └──────────────────┘   │
            └────────────────────────────────────────────┘
                              │
                              ↓
                    ┌──────────────────┐
                    │  Matching Agent  │
                    │   (RAG-enhanced) │
                    └──────────────────┘
                              │
                              ↓
                    ┌──────────────────┐
                    │  Ranked Results  │
                    └──────────────────┘
```

### 1. Resume Processing ([ResumeManager](src/services/resume_service.py))

- **Text Extraction**: PyPDF2 extracts raw text from PDF
- **LLM Parsing**: Ollama (llama3.2) structures the data using prompt templates from [src/prompts/resume.yaml](src/prompts/resume.yaml)
- **Data Storage**: Structured resume saved to SQLite with fields:
  - Personal info (name, email, phone)
  - Skills (list)
  - Experience (structured work history)
  - Education (degrees, institutions)
  - Projects
  - Summary

### 2. Job Scraping ([JobsManager](src/services/job_service.py))

- **Web Scraping**: BeautifulSoup4 scrapes job listings from LinkedIn
- **LLM Extraction**: Parses each job posting to extract:
  - Job description (cleaned summary)
  - Requirements (must-haves)
  - Key technologies (tools, languages, frameworks)
- **Deduplication**: Checks database before adding (by job_id)
- **Prompts**: Uses templates from [src/prompts/job.yaml](src/prompts/job.yaml)

### 3. RAG-Enhanced Matching ([MatchingAgent](src/core/matching/agent.py))

The matching system uses **Retrieval-Augmented Generation (RAG)** for intelligent, context-aware matching:

#### Context Building ([ContextBuilder](src/core/matching/context_builder.py))

For each job-resume pair:

1. **Skill Extraction**: Identifies all skills from both resume and job description
2. **Vector Search**: Queries ChromaDB ([KnowledgeStore](src/core/knowledge/store.py)) for each skill:
   - **Definitions**: What the skill/technology actually means
   - **Related Tools**: Frameworks, libraries, platforms associated with the skill
   - **Manifestations**: Real-world examples of how the skill appears in experience
3. **Context Assembly**: Combines all retrieved information into rich context

#### Scoring

LLM evaluates the match using the enriched context across four dimensions:

- **Technical Skills** (40 points): Skill overlap, proficiency alignment
- **Experience Level** (25 points): Years of experience, role seniority
- **Education** (15 points): Degree relevance, institution prestige
- **Role Alignment** (20 points): Career trajectory, job responsibilities fit

#### Recommendation Levels

- **STRONG MATCH** (80-100): Apply immediately
- **GOOD MATCH** (60-79): Strong candidate
- **MODERATE MATCH** (40-59): Consider applying
- **WEAK MATCH** (20-39): Low fit
- **POOR MATCH** (0-19): Not recommended

### 4. Knowledge Store - RAG Component ([KnowledgeStore](src/core/knowledge/store.py))

The vector database enables **semantic matching beyond keyword matching**:

- **Technology**: ChromaDB (vector database with persistence)
- **Location**: `data/vector_db/`
- **Content**: JSON files in `data/knowledge/skills/` containing:

  ```json
  {
    "skill_name": "Python",
    "definitions": ["High-level programming language..."],
    "related_tools": ["Django", "Flask", "FastAPI", "NumPy"],
    "experience_manifestations": [
      "Built REST APIs using FastAPI",
      "Developed data pipelines with Pandas"
    ]
  }
  ```

- **Benefits**:
  - Understands that "React" and "React.js" are the same
  - Recognizes that "API development" relates to "FastAPI", "REST", "GraphQL"
  - Matches experience descriptions to required skills semantically

**Configuration**: Adjust retrieval limits in [src/config/settings.py](src/config/settings.py#L24-L27)

## Configuration

All configuration is centralized in [src/config/settings.py](src/config/settings.py):

```python
class Config:
    # Directories
    DATA_DIR = PROJECT_ROOT_DIR.joinpath("data")
    PROMPT_DIR = PROJECT_ROOT_DIR.joinpath("src", "prompts")
    VECTOR_DB_DIR = DATA_DIR.joinpath("vector_db")
    KNOWLEDGE_PATH = DATA_DIR.joinpath("knowledge")

    # Job Scraping
    SCRAPER_URLs = {
        "LinkedIn": "https://linkedin.com/jobs-guest/jobs/api/..."
    }

    # Vector Database (ChromaDB)
    CHROMADB_PERSISTANCE_PATH = VECTOR_DB_DIR
    SKILL_COLLECTION_NAME = "skills"

    # RAG Retrieval Limits
    PER_SKILL_DEFINITIONS = 1        # Number of definitions per skill
    PER_SKILL_TOOLS = 1              # Number of related tools per skill
    PER_EXPERIENCE_MANIFESTATIONS = 3  # Number of experience examples
```

### Customization Options

- **Job Sources**: Modify `SCRAPER_URLs` to add new job boards
- **Search Criteria**: Edit LinkedIn URL parameters (keywords, location, time posted)
- **LLM Model**: Change `Ollama(model="llama3.2")` in service files
- **Prompts**: Edit YAML files in [src/prompts/](src/prompts/) to customize LLM behavior
- **RAG Context**: Adjust retrieval limits to balance context richness vs token usage

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Ollama (llama3.2) | Local inference for resume parsing, job extraction, matching |
| **Vector DB** | ChromaDB | Semantic search for skill knowledge retrieval |
| **Database** | SQLite + SQLAlchemy | Resume and job posting persistence |
| **LLM Framework** | LangChain | Prompt management and LLM orchestration |
| **PDF Parsing** | PyPDF2 | Resume text extraction |
| **Web Scraping** | BeautifulSoup4 + Requests | Job posting scraping |
| **Package Manager** | UV | Fast dependency management |

## Project Status

**Current State**: Working POC (Proof of Concept)

✅ **Completed Features**:
- Resume PDF parsing and structured extraction
- LinkedIn job scraping with LLM-based requirement extraction
- RAG-enhanced matching agent with context building
- Vector knowledge store integration
- SQLite database for data persistence

🚧 **In Progress**:
- Full matching pipeline (scoring logic partially implemented)
- Knowledge base population (skill definitions)

📋 **Planned**:
- Complete end-to-end matching workflow
- Results ranking and filtering
- Additional job sources (Indeed, Glassdoor)

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

### Adding Dependencies

```bash
# With UV (recommended)
uv add <package-name>

# With pip
pip install <package-name>
pip freeze > requirements.txt
```

## Troubleshooting

**Ollama connection errors:**
```bash
# Ensure Ollama is running
ollama serve

# Verify model is available
ollama list
ollama pull llama3.2
```

**ChromaDB errors:**
```bash
# Delete and recreate vector DB
rm -rf data/vector_db/
# Restart application to rebuild
```

**Import errors:**
```bash
# Ensure you're in the project root
cd career-copilot

# Reinstall dependencies
uv sync  # or pip install -r requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License

## Author

**Tirth Patel**
- Email: dev.tirthp14@gmail.com

## Future Enhancements

- [ ] Complete end-to-end matching pipeline with scoring
- [ ] Support for more job sources (Indeed, Glassdoor, etc.)
- [ ] Web UI for results visualization
- [ ] Resume optimization suggestions based on target jobs
- [ ] AI-powered cover letter generation
- [ ] Application tracking system
- [ ] Email notifications for high-match new jobs
- [ ] Export results to CSV/JSON
- [ ] Support for DOCX resumes
- [ ] Batch processing for multiple resumes
