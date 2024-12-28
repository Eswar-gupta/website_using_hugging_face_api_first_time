from pathlib import Path

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: str):
        self.error_message = self._format_error(error_message, error_detail)
        super().__init__(self.error_message)

    def _format_error(self, error_message: str, error_detail: str) -> str:
        return f"""
Error occurred in execution of:
{'='*10}
Relative Path: {Path(error_detail).relative_to(Path.cwd())}
Error Message:
{error_message}

Full Path: {Path(error_detail).resolve()}
{'='*10}
"""

