import sys
import traceback

class AppException(Exception):
    """
    Custom application-level exception that captures file name, line number,
    and detailed traceback for debugging purposes.
    """

    def __init__(self, error_message: Exception):
        """
        Initialize AppException with formatted error details.
        
        Args:
            error_message (Exception): The original exception message.
        """
        super().__init__(str(error_message))
        self.error_message = self._get_error_message_detail(error_message)

    @staticmethod
    def _get_error_message_detail(error: Exception) -> str:
        """
        Builds a detailed error message using traceback information.

        Args:
            error (Exception): The original raised exception.

        Returns:
            str: Formatted error message with script name and line number.
        """
        exc_type, exc_obj, exc_tb = sys.exc_info()

        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            return f"Error in script [{file_name}] at line [{line_number}]: {error}"
        else:
            return f"Error: {error} (no traceback available)"

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.error_message}')"
    

class CSVReadError(AppException):
    def __init__(self, file_path: str):
        super().__init__(f"Failed to read CSV file: {file_path}")


class PDFReadError(AppException):
    def __init__(self, file_path: str):
        super().__init__(f"Failed to read PDF file: {file_path}")


class JSONReadError(AppException):
    def __init__(self, file_path: str):
        super().__init__(f"Failed to read JSON file: {file_path}")


class TextReadError(AppException):
    def __init__(self, file_path: str):
        super().__init__(f"Failed to read text file: {file_path}")

