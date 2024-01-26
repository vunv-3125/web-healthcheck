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
    message_format = "%(asctime)s %(message)s"
    date_format = "[%Y-%m-%d %H:%M:%S]"
    logging.basicConfig(
        filename="logs/info.log",
        format=message_format,
        datefmt=date_format,
        level=logging.INFO,
    )
    logging.basicConfig(
        filename="logs/error.log",
        format=message_format,
        datefmt=date_format,
        level=logging.ERROR,
    )

    selenium_logger = logging.getLogger("seleniumwire")
    if selenium_logger.hasHandlers():
        selenium_logger.handlers.clear()
    selenium_logger.addHandler(logging.FileHandler("logs/selenium_debug.log"))


def generate_auth_header(username: str, password: str) -> str:
    return f'Basic {base64.b64encode(f"{username}:{password}".encode("ascii")).decode("ascii")}'
