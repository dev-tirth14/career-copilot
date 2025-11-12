from .database.models import DatabaseManager
from .agents.ResumeManager import ResumeManager
from .utils.config import Config
from pathlib import Path
# db_manager=DatabaseManager()
# sample_resume={
#     "raw_text":"",
#     "name":"Tirth Patel",
#     "email":"dev.tirthp14@gmail.com",
#     "phone_number":"6475337957",
#     "skills":"Python, SQL",
#     "education":"BSc from Ontario Tech University",
#     "experience":"2 years at IBM as an Associate Software Developer",
#     "summary":"I want to work in Faang"
# }
# db_manager.add_resume(sample_resume)

# resumes=db_manager.get_all_resumes()
# print(resumes[0].id)

# db_manager.close_connection()

resume_manager=ResumeManager()
Path("data/resumes/john_resume.pdf")
file_path=Config.DATA_DIR.joinpath("resumes","resume_2025.pdf")
resume_manager.process_resume(file_path=file_path)
