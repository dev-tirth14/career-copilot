from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Resume(Base):
    """Resume entity representing a candidate's resume in the database."""
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_text = Column(Text)
    name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)
    skills = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    summary = Column(Text)
    projects = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean)


class Job(Base):
    """Job entity representing a job posting in the database."""
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    job_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    description = Column(Text)
    requirements = Column(Text)
    key_technologies = Column(Text)
    url = Column(String, unique=True)
    source = Column(String)  # 'remoteok', 'hackernews', etc.

    scraped_at = Column(DateTime, default=datetime.now)
    processed = Column(Boolean, default=False)
    match_score = Column(Float, nullable=True)
