from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
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



# Databse operations
class DatabaseManager:
    def __init__(self):
        db_path=Config.DATA_DIR.joinpath("database.db")
        try:
            engine = create_engine(f"sqlite:///{db_path}", echo=True)
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
    
    def close_connection(self):
        try:
            self.session.close()
        except Exception as e:
            print("Close session connection UNSUCCESSFUL: \n", e)