from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .entities import Base, Resume, Job
from ..config.settings import Config
import json


class DatabaseManager:
    """Manages database connections and operations for resumes and jobs."""

    def __init__(self):
        db_path = Config.DATA_DIR.joinpath("database.db")
        try:
            engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(engine)
            self.session = sessionmaker(bind=engine)()
            print(f"Connection to the db successful.")
        except Exception as ex:
            print("Connection could not be made due to the following error: \n", ex)

    def add_resume(self, resume_details: dict):
        """Add a new resume and set it as active."""
        new_resume = Resume(
            raw_text=resume_details.get("raw_text"),
            name=resume_details.get("name"),
            email=resume_details.get("email"),
            phone_number=resume_details.get("phone_number"),
            skills=json.dumps(resume_details.get("skills")),
            education=resume_details.get("education"),
            experience=json.dumps(resume_details.get("experience")),
            summary=resume_details.get("summary"),
            projects=json.dumps(resume_details.get("projects")),
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
        """Retrieve all resumes from the database."""
        try:
            resumes: list[Resume] = self.session.query(Resume).all()
            return resumes
        except Exception as e:
            print("Commit for retrieving all resumes UNSUCCESSFUL: \n", e)
            return []

    def get_active_resume(self):
        """Retrieve the currently active resume."""
        try:
            resume: Resume = self.session.query(Resume).where(Resume.is_active).first()
            return resume
        except Exception as e:
            print("Retrieving ACTIVE resume UNSUCCESSFUL: \n", e)
            return None

    def add_job_posting(self, job_details: dict):
        """Add a new job posting to the database."""
        new_job_posting = Job(
            job_id=job_details.get("job_id"),
            title=job_details.get("title"),
            company=job_details.get("company"),
            location=job_details.get("location"),
            description=job_details.get("description"),
            requirements=json.dumps(job_details.get("requirements")),
            key_technologies=json.dumps(job_details.get("key_technologies")),
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
        """Retrieve all jobs from the database."""
        try:
            jobs: list[Job] = self.session.query(Job).all()
            return jobs
        except Exception as e:
            print("Retrieving all jobs UNSUCCESSFUL: \n", e)
            return []

    def get_all_unprocessed_jobs(self):
        """Retrieve all jobs that haven't been processed for matching yet."""
        try:
            jobs: list[Job] = self.session.query(Job).where(Job.processed == False).all()
            return jobs
        except Exception as e:
            print("Retrieving UNPROCESSED jobs UNSUCCESSFUL: \n", e)
            return []

    def does_job_exist(self, job_id: str):
        """Check if a job with the given ID exists in the database."""
        try:
            job: Job = self.session.query(Job).where(Job.job_id == job_id).first()
            return job is not None
        except Exception as e:
            print(f"Retrieving job {job_id} UNSUCCESSFUL: \n", e)
            return False

    def close_connection(self):
        """Close the database session."""
        try:
            self.session.close()
        except Exception as e:
            print("Close session connection UNSUCCESSFUL: \n", e)
