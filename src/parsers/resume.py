from pathlib import Path
from dataclasses import dataclass
import logging
import os
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

@dataclass
class ParsedResume:
    raw_text:str

class ResumeParser:
    def __init__(self):
        pass
    def extract_resume(self,file_path:Path) -> ParsedResume:
        logging.info(f"Extracting resume: {file_path.name} ...")
        #check if file exists
        if not file_path.exists():
            logging.error(f"Resume not found: {file_path}")
            raise FileNotFoundError()

        # determine which parser you need
        file_extension=file_path.suffix.lower()
        if(file_extension==".pdf"):
            return ParsedResume(raw_text=self._extract_from_pdf(file_path=file_path))
        return None
    
    def _extract_from_pdf(self, file_path:Path) -> str:
        if not PyPDF2:
            raise ImportError("PyPDF2 not installed")
        from PyPDF2.errors import PdfReadError
        from PyPDF2 import PdfReader
        # determine which parser you need
        try:
            reader=PdfReader(file_path)
            raw_txt=""
            for page in reader.pages:
                extracted_txt=page.extract_text()
                raw_txt+=extracted_txt
            logging.info(f"Successfully extracted resume details from {file_path.name}.")
            return raw_txt
        except Exception as e:
            logging.error(f"Failed to extract resume details from {file_path.name}.")
            raise PdfReadError(f"Error reading PDF: {e}")

        
