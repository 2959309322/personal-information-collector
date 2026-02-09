import time
from functools import wraps
from dataclasses import dataclass
from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, Date
@dataclass
class hotdata:
    date: Date
    name: String
    rank: Integer
    url: String
    info: dict

class collector:
    def __init__(self, source:str):
        self.source = source

    def collect(self) -> list[hotdata]:
        pass

def timer(func):
    @wraps
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            gap = time.time() - start
            print(f"doing {func.__name__} using time: {gap:.2f} seconds")
    return wrapper

def retry(max_retry: int = 3,delay: float = 1.0):
    def decorator(func):
        @wraps
        def wrapper(*args, **kwargs):
            for i in range(max_retry):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"the {i} time to retry {func.__name__} but failed")
                    print(f"error: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator