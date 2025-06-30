import os
from typing import List, Dict
import pandas as pd
from PyPDF2 import PdfReader
import json

from log import logging
from exception_handler import (
    AppException, 
    PDFReadError, 
    CSVReadError, 
    TextReadError,
    JSONReadError
    )

logger = logging.getLogger(__name__)


class DocumentLoader:
    def __init__(self, data_directory: str):
        """
        📁 Initialize the DocumentLoader with a data directory path.

        Args:
            data_directory (str): Root path where department folders are located.
        """
        try: 
            logger.info(f"{'='*20} DocumentLoader Initialization Started {'='*20}")
            self.data_directory = data_directory
            logger.info(f"📂 Data directory set to: {data_directory}")
        except Exception as e:
            logger.exception("❌ Exception during DocumentLoader initialization.")
            raise AppException(e) from e

    def load_documents_by_department(self, department: str) -> List[Dict]:
        """
        🗂️ Load all documents from a specified department folder.

        Args:
            department (str): Name of the department (folder name).

        Returns:
            List[Dict]: List of dictionaries containing document content and metadata.
        """
        try:
            dept_path = os.path.join(self.data_directory, department)
            documents = []

            logger.info(f"📁 Loading documents from department: {department}")

            for file in os.listdir(dept_path):
                file_path = os.path.join(dept_path, file)
                content = self._load_file(file_path)

                documents.append({
                    "content": content,
                    "source": file,
                    "department": department,
                    "metadata": {"file_path": file_path}
                })

            logger.info(f"✅ Loaded {len(documents)} documents from {department}")
            return documents

        except Exception as e:
            logger.exception(f"❌ Error loading documents for department: {department}")
            raise AppException(e) from e

    def _load_file(self, file_path: str) -> str:
        """
        📄 Load the content of a document based on file extension.

        Args:
            file_path (str): Path to the document.

        Returns:
            str: Loaded text content from the file.
        """
        try:
            ext = os.path.splitext(file_path)[1].lower()
            logger.info(f"📑 Reading file: {file_path} (ext: {ext})")

            if ext == '.pdf':
                return self._load_pdf(file_path)
            elif ext == '.csv':
                return self._load_csv(file_path)
            elif ext == '.json':
                return self._load_json(file_path)
            elif ext == '.md':
                return self._load_text(file_path)
            else:
                return self._load_text(file_path)

        except Exception as e:
            logger.exception(f"❌ Failed to load file: {file_path}")
            raise AppException(e) from e

    def _load_pdf(self, file_path: str) -> str:
        """
        📘 Load text from a PDF file.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            str: Extracted text from the PDF.
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            logger.exception(f"❌ Failed to read PDF file: {file_path}")
            raise PDFReadError(file_path) from e

    def _load_csv(self, file_path: str) -> str:
        """
        📊 Load data from a CSV file and convert it to a string.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            str: CSV content as string.
        """
        try:
            df = pd.read_csv(file_path)
            return df.to_string()
        except Exception as e:
            logger.exception(f"❌ Failed to read CSV file: {file_path}")
            raise CSVReadError(file_path) from e

    def _load_json(self, file_path: str) -> str:
        """
        🧾 Load and format JSON file content.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            str: Pretty-formatted JSON content.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return json.dumps(data, indent=2)
        except Exception as e:
            logger.exception(f"❌ Failed to read JSON file: {file_path}")
            raise JSONReadError(file_path) from e

    def _load_text(self, file_path: str) -> str:
        """
        📄 Load plain text or Markdown content.

        Args:
            file_path (str): Path to the text or markdown file.

        Returns:
            str: Raw file content as a string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.exception(f"❌ Failed to read text file: {file_path}")
            raise TextReadError(file_path) from e
