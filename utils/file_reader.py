import PyPDF2
from docx import Document
import os

class FileReader:
    """Class to handle reading PDF and DOCX files"""
    
    def __init__(self):
        """Initialize FileReader"""
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def read_file(self, file_path):
        """
        Read file and return text content
        """
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
      
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        
        # Read based on file type
        if extension == '.pdf':
            return self.read_pdf(file_path)
        elif extension == '.docx':
            return self.read_docx(file_path)
        elif extension == '.txt':
            return self.read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def read_pdf(self, file_path):
        """
        Extract text from PDF file

        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from each page
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
            
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def read_docx(self, file_path):
        """
        Extract text from DOCX file
        """
        try:
            doc = Document(file_path)
            text = ""
            
            # Extract text from each paragraph
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def read_txt(self, file_path):
        """
        Read plain text file

        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def is_supported(self, file_path):
        """
        Check if file format is supported
        """
        _, extension = os.path.splitext(file_path)
        return extension.lower() in self.supported_formats



if __name__ == "__main__":
    reader = FileReader()
    print("File Reader initialized successfully!")
    print(f"Supported formats: {reader.supported_formats}")
