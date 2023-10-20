import base64
from dotenv import load_dotenv
import requests
from utils import is_executed_without_exception, max_retry

load_dotenv()


@is_executed_without_exception
@max_retry(5)
def is_accessible(url: str, basic_auth_username: str, basic_auth_password: str):
    auth_header = generate_auth_header(basic_auth_username, basic_auth_password)
    headers = {
        "Authorization": auth_header,
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    }
    response = requests.get(url, headers=headers)
    response_code = response.status_code

    if response_code // 100 != 2:
        raise Exception()


def generate_auth_header(username: str, password: str) -> str:
    return f'Basic {base64.b64encode(f"{username}:{password}".encode("ascii")).decode("ascii")}'
