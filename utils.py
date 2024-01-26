import base64
import logging
from time import sleep

SELENIUM_LOGGING_LEVEL = 21


def max_retry(max_times):
    def retry(func):
        def wrapper(*args, **kwargs):
            for _ in range(max_times):
                try:
                    return func(*args, **kwargs)
                except:
                    sleep(3)

            raise Exception()

        return wrapper

    return retry


def is_executed_without_exception(func):
    def wrapper(*args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)

            return True
        except:
            return False

    return wrapper


def setup_logging():
    formatter = logging.Formatter("%(asctime)s:%(levelname)s %(message)s")
    formatter.datefmt = "[%Y-%m-%d %H:%M:%S]"

    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    selenium_logger = logging.getLogger("seleniumwire")
    selenium_logger.setLevel(logging.INFO)
    if selenium_logger.hasHandlers():
        selenium_logger.handlers.clear()
    file_handler = logging.FileHandler("logs/selenium.log")
    file_handler.setFormatter(formatter)
    selenium_logger.addHandler(file_handler)


def generate_auth_header(username: str, password: str) -> str:
    return f'Basic {base64.b64encode(f"{username}:{password}".encode("ascii")).decode("ascii")}'
