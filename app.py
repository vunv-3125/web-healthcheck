from datetime import datetime
import logging
import os
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

    site_names = os.environ.get("SITE_NAMES", "").split(",")
    site_urls = os.environ.get("SITE_URLS", "").split(",")
    basic_auth_usernames = os.environ.get("BASIC_AUTH_USERNAMES", "").split(",")
    basic_auth_passwords = os.environ.get("BASIC_AUTH_PASSWORDS", "").split(",")

    try:
        websites = "\n".join(
            [
                f"{site_name}: {site_url}"
                for site_name, site_url in zip(site_names, site_urls)
            ]
        )
        logging.info(f"Websites list:\n {websites}")

        inaccessible_websites = [
            (site_name, site_url)
            for site_name, site_url, basic_auth_username, basic_auth_password in zip(
                site_names, site_urls, basic_auth_usernames, basic_auth_passwords
            )
            if not is_accessible(site_url, basic_auth_username, basic_auth_password)
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
