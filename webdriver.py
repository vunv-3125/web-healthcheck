import base64
from seleniumwire.request import Request
from seleniumwire.webdriver import Firefox, FirefoxOptions

from singleton_meta import SingletonMeta


def add_auth_header(request: Request):
    request.headers["Authorization"] = WebDriverSingleton().auth_header


class WebDriverSingleton(metaclass=SingletonMeta):
    driver: Firefox
    auth_header: str = ""

    def __init__(self) -> None:
        options = FirefoxOptions()
        options.set_preference("permissions.default.image", 2)
        options.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")
        options.add_argument("--headless")
        self.driver = Firefox(options=options)
        self.driver.request_interceptor = add_auth_header

    def set_auth_header(self, username: str, password: str) -> None:
        auth_header = f'Basic {base64.b64encode(f"{username}:{password}".encode("ascii")).decode("ascii")}'
        self.auth_header = auth_header
