from ..models.database import DatabaseManager
from ..models.entities import Resume
from ..parsers.resume import ResumeParser
from ..config.settings import Config
from pathlib import Path
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
import yaml
import time
import json

class ResumeManager:
    def __init__(self):
        self.parser=ResumeParser()
        self.db_manager=DatabaseManager()
        self.llm = Ollama(model="llama3.2")

        prompts_file=Config.PROMPT_DIR.joinpath("resume.yaml")
        if(not prompts_file.exists()):
            raise Exception("ResumeManager prompt file foes not exist")
        with open(prompts_file, 'r') as file:
            self.prompts = yaml.safe_load(file)
        
    def process_resume(self, file_path:Path):
        parsed_resume=self.parser.extract_resume(file_path=file_path)

        resume_details=self.llm_parse(parsed_resume.raw_text)

        print(json.dumps(resume_details, indent=4))

        self.db_manager.add_resume(resume_details=resume_details)

        name=self.db_manager.get_all_resumes()[0].name
    
    def get_active_resume(self) -> Resume:
        return self.db_manager.get_active_resume()

    def llm_parse(self, resume_text:str):
        prompt=PromptTemplate.from_template(self.prompts.get("basic_resume_extraction")).format(resume_text=resume_text)
        start_time = time.perf_counter()
        try:
            resp=self.llm.invoke(prompt)
            print(resp)
            resp_obj=json.loads(resp)
        except Exception as e:
            print("LLM Inference ERROR")
            raise Exception(e)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        resume_details={
            "raw_text":resume_text,
            "name":resp_obj.get("name"),
            "email":resp_obj.get("email"),
            "phone_number":resp_obj.get("phone_number"),
            "skills":resp_obj.get("skills"),
            "education":resp_obj.get("education"),
            "experience":resp_obj.get("experience"),
            "summary":resp_obj.get("summary"),
            "projects":resp_obj.get("projects")
        }

        # Print the duration in seconds
        print(f"The operation took {elapsed_time:.4f} seconds.")
        return resume_details


