import os
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from typing import List, Dict, Union, Any
import json
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileAnalyzer:
    """Main class for analyzing different types of files"""
    
    @staticmethod
    def read_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading PDF file: {e}")
            return ""

    @staticmethod
    def read_docx(file_path: str) -> str:
        """
        Extract text from a DOCX file
        """
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            logger.error(f"Error reading DOCX file: {e}")
            return ""

    @staticmethod
    def read_text(file_path: str) -> str:
        """
        Read text from a plain text file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            return ""

class TextAnalyzer:
    """Class for analyzing text content"""
    
    @staticmethod
    def get_word_count(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def get_character_count(text: str, include_spaces: bool = True) -> int:
        """Count characters in text"""
        if include_spaces:
            return len(text)
        return len(text.replace(" ", ""))

    @staticmethod
    def get_line_count(text: str) -> int:
        """Count lines in text"""
        return len(text.splitlines())

class DataProcessor:
    """Class for processing and transforming data"""
    
    @staticmethod
    def text_to_dataframe(text: str, delimiter: str = "\n") -> pd.DataFrame:
        """Convert text to DataFrame"""
        try:
            lines = text.split(delimiter)
            # Assume first line is header
            if lines:
                header = lines[0].split(",")
                data = [line.split(",") for line in lines[1:]]
                return pd.DataFrame(data, columns=header)
        except Exception as e:
            logger.error(f"Error converting text to DataFrame: {e}")
        return pd.DataFrame()

    @staticmethod
    def save_analysis_results(results: Dict[str, Any], output_path: str) -> bool:
        """Save analysis results to JSON"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Error saving analysis results: {e}")
            return False

class FileManager:
    """Class for managing file operations"""
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Union[str, int]]:
        """Get file information"""
        try:
            file_stats = os.stat(file_path)
            return {
                "name": os.path.basename(file_path),
                "size": file_stats.st_size,
                "created": datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                "modified": datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                "extension": os.path.splitext(file_path)[1],
                "path": os.path.abspath(file_path)
            }
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {}

    @staticmethod
    def is_valid_file(file_path: str, allowed_extensions: List[str]) -> bool:
        """Check if file is valid and has allowed extension"""
        if not os.path.exists(file_path):
            return False
        return os.path.splitext(file_path)[1].lower() in allowed_extensions

def format_size(size_in_bytes: int) -> str:
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"
