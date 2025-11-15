from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..utils.config import Config

Base = declarative_base()

# Database table definition
class Resume(Base):
    __tablename__ = 'resumes'

    id= Column(Integer, primary_key=True, autoincrement=True)
    raw_text=Column(Text)
    name= Column(String, nullable=False)
    email= Column(String)
    phone_number=Column(String)
    skills=Column(Text)
    education=Column(Text)
    experience=Column(Text)
    summary=Column(Text)
    projects=Column(Text)
    uploaded_at=Column(DateTime,default=datetime.now())
    is_active=Column(Boolean)

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    job_id=Column(String, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    description = Column(Text)
    requirements = Column(Text)
    key_technologies= Column(Text)
    url = Column(String, unique=True)
    source = Column(String)  # 'remoteok', 'hackernews', etc.
    
    scraped_at = Column(DateTime, default=datetime.now)
    processed = Column(Boolean, default=False)  # For Phase 2 matching
    match_score = Column(Float, nullable=True)  # For Phase 2

# Databse operations
class DatabaseManager:
    def __init__(self):
        db_path=Config.DATA_DIR.joinpath("database.db")
        try:
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            self.session=sessionmaker(bind=engine)()
            print(f"Connection to the db successfull.")
        except Exception as ex:
            print("Connection could not be made due to the following error: \n", ex)
    
    def add_resume(self,resume_details:dict):
        #create new resume obj to be active
        new_resume=Resume(
            raw_text=resume_details.get("raw_text"),
            name=resume_details.get("name"),
            email=resume_details.get("email"),
            phone_number=resume_details.get("phone_number"),
            skills=resume_details.get("skills"),
            education=resume_details.get("education"),
            experience=resume_details.get("experience"),
            summary=resume_details.get("summary"),
            projects=resume_details.get("projects"),
            uploaded_at=resume_details.get("uploaded_at"),
            is_active=True
            )
        try:
            self.session.query(Resume).update({Resume.is_active: False})
            self.session.add(new_resume)
            self.session.commit()
            print("Resume successfully added.")
        except Exception as e:
            print("Commit for adding a new resume UNSUCCESSFUL: \n", e)
            self.session.rollback()

    def get_all_resumes(self):
        try:
            resumes:list[Resume]=self.session.query(Resume).all()
            return resumes
        except Exception as e:
            print("Commit for retrieving all resumes UNSUCCESSFUL: \n", e)
            return []
    
    def add_job_posting(self,job_details:dict):
        #create new resume obj to be active
        new_job_posting=Job(
            job_id=job_details.get("job_id"),
            title=job_details.get("title"),
            company=job_details.get("company"),
            location=job_details.get("location"),
            description=job_details.get("description"),
            requirements=job_details.get("requirements"),
            key_technologies=job_details.get("key_technologies"),
            url=job_details.get("url"),
            source=job_details.get("source"),
            scraped_at=job_details.get("scraped_at"),
            )
        try:
            self.session.add(new_job_posting)
            self.session.commit()
            print("Job successfully added.")
        except Exception as e:
            print("Commit for adding a new job posting UNSUCCESSFUL: \n", e)
            self.session.rollback()

    def get_all_jobs(self):
        try:
            jobs:list[Job]=self.session.query(Job).all()
            return jobs
        except Exception as e:
            print("Retrieving all jobs UNSUCCESSFUL: \n", e)
            return []
    
    def does_job_exist(self, job_id:str):
        try:
            job:Job=self.session.query(Job).where(Job.job_id==job_id).first()
            return job is not None
        except Exception as e:
            print(f"Retrieving job {job_id} UNSUCCESSFUL: \n", e)
            return False
    
    def close_connection(self):
        try:
            self.session.close()
        except Exception as e:
            print("Close session connection UNSUCCESSFUL: \n", e)