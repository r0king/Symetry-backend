"""
Define custom exceptions
"""
class IntendedException(Exception):
    """
    Base Exception
    """
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
