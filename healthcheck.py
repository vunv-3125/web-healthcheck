import logging
from typing import Optional
from dotenv import load_dotenv
from seleniumwire.request import Response
from utils import is_executed_without_exception, max_retry
from webdriver import WebDriverSingleton

load_dotenv()


@is_executed_without_exception
@max_retry(3)
def is_accessible(url: str, basic_auth_username: str, basic_auth_password: str):
    singleton = WebDriverSingleton()
    singleton.set_auth_header(basic_auth_username, basic_auth_password)
    driver = singleton.driver
    driver.get(url)
    try:
        response: Optional[Response] = next(
            (
                request.response
                for request in driver.requests
                if request.url == driver.current_url
            )
        )
        if response:
            response_code = response.status_code
            logging.info(f"{url}: {response_code}")
            if response_code // 100 == 2:
                return
        raise Exception()
    except:
        raise Exception()
