from ..database.models import DatabaseManager
from ..tools.ResumeParser import ResumeParser
from pathlib import Path

class ResumeManager:
    def __init__(self):
        self.parser=ResumeParser()
        self.db_manager=DatabaseManager()
    
    def process_resume(self, file_path:Path):
        parsed_resume=self.parser.parse_resume(file_path=file_path)
        print(parsed_resume.raw_text)
