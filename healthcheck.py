import logging
from typing import Optional
from dotenv import load_dotenv
from seleniumwire.request import Response as SeleniumResponse
from utils import (
    generate_auth_header,
    is_executed_without_exception,
    max_retry,
)
from webdriver import WebDriverSingleton
import requests

load_dotenv()


def doRequest(
    url: str,
    basic_auth_username: str = "",
    basic_auth_password: str = "",
) -> int:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Authorization": f"Basic {generate_auth_header(basic_auth_username, basic_auth_password)}",
    }

    return requests.get(url, headers=headers).status_code


def doSeleniumRequest(
    url: str,
    basic_auth_username: str = "",
    basic_auth_password: str = "",
) -> int:
    singleton = WebDriverSingleton()
    singleton.set_auth_header(basic_auth_username, basic_auth_password)
    driver = singleton.driver
    driver.get(url)

    response: Optional[SeleniumResponse] = next(
        (request.response for request in driver.requests if request.url.startswith(url))
    )

    return response.status_code if response else 0


@is_executed_without_exception
@max_retry(3)
def is_accessible(
    url: str,
    basic_auth_username: str = "",
    basic_auth_password: str = "",
    use_selenium=False,
):
    try:
        response_code = (
            doSeleniumRequest(url, basic_auth_username, basic_auth_password)
            if use_selenium
            else doRequest(url, basic_auth_username, basic_auth_password)
        )
        logging.getLogger("app").info(f"{url}: {response_code}")
        if response_code // 100 == 2:
            return
        raise Exception()
    except:
        raise Exception()
