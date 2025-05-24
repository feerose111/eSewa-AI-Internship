from typing import List
from datetime import datetime


class LogSubject:
    """Subject class that observers will subscribe to"""
    _observers: List['LogObserver'] = []

    @classmethod
    def attach(cls, observer: 'LogObserver'):
        if observer not in cls._observers:
            cls._observers.append(observer)

    @classmethod
    def detach(cls, observer: 'LogObserver'):
        if observer in cls._observers:
            cls._observers.remove(observer)

    @classmethod
    def notify(cls, message: str, level: str = "INFO"):
        for observer in cls._observers:
            observer.update(message, level)


class LogObserver:
    """Base observer class"""

    def update(self, message: str, level: str):
        pass


class FileLogger(LogObserver):
    """Logs messages to a file"""

    def __init__(self, file_path: str = "wallet.log"):
        self.file_path = file_path

    def update(self, message: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        with open(self.file_path, "a") as f:
            f.write(log_entry)


# Initialize default logger
LogSubject.attach(FileLogger())
