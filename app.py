from datetime import datetime
import json
import logging
import os
from typing import List
from dotenv import load_dotenv
import pytz
from healthcheck import is_accessible
from slack_api import build_message, send_message
from utils import setup_logging
from webdriver import WebDriverSingleton

if __name__ == "__main__":
    load_dotenv()
    driver = WebDriverSingleton().driver
    setup_logging()

    timezone = pytz.timezone("Asia/Tokyo")
    now = datetime.now(timezone).strftime("%Y/%m/%d %H:%M %Z")

    with open("sites_data.json", "r") as sites_data_file:
        sites_data: List[dict] = json.load(sites_data_file)

    websites = (site_data.values() for site_data in sites_data)
    try:
        inaccessible_websites = [
            (name, url, basic_auth_username, basic_auth_password, use_selenium)
            for name, url, basic_auth_username, basic_auth_password, use_selenium in websites
            if not is_accessible(
                url,
                basic_auth_username,
                basic_auth_password,
                use_selenium,
            )
        ]

        if len(inaccessible_websites) > 0:
            send_message(
                os.environ.get("SLACK_CHANNEL_ID", ""),
                build_message(inaccessible_websites, now),
            )
    except Exception as ex:
        logging.error(ex)
    finally:
        driver.quit()
