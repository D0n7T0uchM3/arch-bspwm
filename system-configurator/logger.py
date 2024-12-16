from time import strftime
from enum import Enum, auto
from typing import Optional


class LoggerStatus(Enum):
    ERROR = auto()
    SUCCESS = auto()
    FAILURE = auto()

    def __str__(self):
        return self.name


class Logger:
    def __init__(self, filename: Optional[str] = "build_debug.log"):
        self.filename = filename

    def add_record(self, text: str, *, status: LoggerStatus) -> None:
        formatted_text = self.__format_log_entry(text, status)
        print(formatted_text, end='')  # Output to console for visibility

        with open(self.filename, "a", encoding="UTF-8") as file:
            file.write(formatted_text)

    def __format_log_entry(self, text: str, status: LoggerStatus) -> str:
        timestamp = strftime("%Y-%m-%d %H:%M:%S")  # Customizable timestamp format
        return f"[{status}] | {text} | {timestamp}\n"


# Example Usage:
# logger = Logger("custom_log.log")
# logger.add_record("Installation started", status=LoggerStatus.SUCCESS)
# logger.add_record("Installation failed", status=LoggerStatus.ERROR)
