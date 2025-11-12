from pathlib import Path
from dataclasses import dataclass
import os
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

@dataclass
class ParsedResume:
    raw_text:str

class ResumeParser:
    print("")
    def __init__(self):
        pass
    def parse_resume(self,file_path:Path) -> ParsedResume:
        #check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError()

        # determine which parser you need
        file_extension=file_path.suffix.lower()
        if(file_extension==".pdf"):
            return ParsedResume(raw_text=self._extract_from_pdf(file_path=file_path))
        elif(file_extension==".docx"):
            return ParsedResume(raw_text=self._extract_from_docx(file_path=file_path))
        
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
            return raw_txt
        except Exception as e:
            raise PdfReadError(f"Error reading PDF: {e}")
    
    def _extract_from_docx(self, file_path:Path)-> str:
        if not docx:
            raise ImportError("docx not installed")
        from docx.exceptions import PythonDocxError
        # TODO
        return None

        
