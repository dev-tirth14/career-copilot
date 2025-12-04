# Career Copilot

An agentic AI job matching system that uses RAG (Retrieval-Augmented Generation) to intelligently match resumes with job postings. Built with local LLMs (Ollama) and vector databases (ChromaDB) for privacy-focused, intelligent job screening.

## Features

- **Resume Parsing**: LLM-powered extraction of structured data from PDF resumes
- **Job Scraping**: Automated scraping from LinkedIn with intelligent requirement extraction
- **RAG-Enhanced Matching**: Context-aware matching using vector search for semantic skill analysis
- **Intelligent Scoring**: Multi-dimensional evaluation across technical skills (40%), experience (25%), education (15%), and role alignment (20%)

## Architecture

```
Resume Parser ──┐
                ├──> SQLite Database ──> Matching Agent (RAG) ──> Ranked Results
Job Scraper ────┘                             ↑
                                              │
                                    Vector Knowledge Base
                                        (ChromaDB)
```

**How RAG Works:**
1. **Context Building**: For each job-resume pair, queries ChromaDB for skill definitions, related tools, and real-world manifestations
2. **Semantic Matching**: Goes beyond keyword matching to understand skill relationships (e.g., "React.js" = "React", "API development" relates to "FastAPI", "REST", "GraphQL")
3. **Intelligent Scoring**: LLM evaluates enriched context to generate detailed compatibility scores and recommendations

## Tech Stack

**AI/ML**: LangChain • Ollama (LLaMA 3.2) • ChromaDB • RAG Architecture
**Backend**: Python • SQLite
**Utilities**: BeautifulSoup4 • PyPDF2

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) (for local LLM)
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd career-copilot

# Install UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Set up Ollama
ollama pull llama3.2
ollama serve

# Add your resume to data/resumes/
cp ~/path/to/resume.pdf data/resumes/
```

### Usage

Update the resume filename in [src/main.py:23](src/main.py#L23), then run:

```bash
python src/main.py
```

This runs the full pipeline:
1. **Process Resume** → Parses PDF and extracts structured data
2. **Scrape Jobs** → Fetches jobs from LinkedIn (configured in [src/config/settings.py](src/config/settings.py))
3. **Match Jobs** → Generates compatibility scores using RAG-enhanced analysis

## Project Structure

```
career-copilot/
├── src/
│   ├── core/
│   │   ├── matching/          # RAG-powered matching agent
│   │   └── knowledge/         # ChromaDB vector store
│   ├── services/              # Resume & job management
│   ├── scrapers/              # Web scrapers (LinkedIn)
│   ├── parsers/               # PDF resume parser
│   ├── models/                # Database models (SQLAlchemy)
│   ├── prompts/               # LLM prompt templates
│   └── config/                # Configuration
├── data/
│   ├── resumes/               # Resume PDFs
│   ├── knowledge/             # Skill definitions (JSON)
│   └── vector_db/             # ChromaDB storage
└── pyproject.toml             # UV dependencies
```

## Configuration

Edit [src/config/settings.py](src/config/settings.py) to customize:
- Job scraping URLs and search criteria
- LLM model selection
- RAG retrieval limits
- Vector database settings

Customize LLM prompts in [src/prompts/](src/prompts/) (YAML files).

## Current Status

**Working POC (Proof of Concept)**

✅ Resume parsing • Job scraping • RAG matching • Vector knowledge store
🚧 Full scoring pipeline • Knowledge base population
📋 Planned: Additional job sources • Web UI • Results export

## Future Enhancements

- Support for Indeed, Glassdoor, and other job boards
- Web UI for results visualization
- Resume optimization suggestions
- AI-powered cover letter generation
- Email notifications for high-match jobs

## License

MIT License

## Author

**Tirth Patel**
Email: dev.tirthp14@gmail.com
