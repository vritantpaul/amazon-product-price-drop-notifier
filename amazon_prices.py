import os
import time
import logging
import contextlib
import pandas as pd
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from winotify import Notification, audio


def log_config():
    # CREATING A LOGGER OBJECT ---
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # setting logging level to "INFO"
    # CREATING A FORMATTER OBJECT ---
    custom_format = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(message)s", datefmt="%d-%b-%y %H:%M:%S"
    )
    # CREATING A HANDLER OBJECT ---
    file_handler = logging.FileHandler("run_log.log")
    file_handler.setFormatter(custom_format)  # setting up format rules
    # ADDING THE FILE HANDLER TO THE LOGGER ---
    logger.addHandler(file_handler)
    return logger


def internet_on():
    with contextlib.suppress(ConnectionError):
        response = requests.get("https://www.google.com/", timeout=3)
        return response.ok


def scrape_info(session, url):
    # MAKING A GET REQUEST ---
    try:
        response = session.get(url)
    except RequestException as e:
        logger.error(f"While scraping URL: {url}: {e}.")
    else:
        try:
            soup = BeautifulSoup(response.text, "lxml")
            # GETTING NAME & PRICE ---
            name = soup.select_one("span#productTitle").text.strip()
            price = soup.select_one("span.a-price span").text
            return name, price
        except AttributeError as e:
            logger.error(f"No Matching Selectors found for {url}.")


def show_toast(name, price, url):
    # SETTING UP TOAST NOTIFICATION ---
    toast = Notification(
        app_id="Script",
        title="Amazon Price Drop!",
        msg=f"Price of the product {name} has dropped to {price}.",
        icon=r"C:\Users\hp\Scripts\miniprograms\Amazon Product Price\Amazon_Logo.png",
    )
    # CONFIGURING ADDITIONAL SETTINGS ---
    toast.set_audio(audio.Mail, loop=False)
    toast.add_actions(label="Go to Amazon⇲", launch=url)
    toast.show()


def main():
    # GETTING PRODUCT LINKS FROM A CSV FILE ---
    df = pd.read_csv("Product Links.csv")

    # CREATING A SESSION OBJECT ---
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/74.0.3729.157 Safari/537.36"
    }
    session = requests.Session()
    session.headers.update(headers)

    # SCRAPE EACH PRODUCT ---
    for url, desired_price in zip(df["URL"], df["Price"]):
        try:
            # name and actual price of the product
            name, price = scrape_info(session, url)
        except TypeError:
            pass
        else:
            name = name.split(":")[0] if ":" in name else name
            actual_price = float(price[1:].replace(",", ""))
            # show toast if actual price below or equal to desired price
            if actual_price <= desired_price:
                show_toast(name, price, url)
            logger.info(f"Ran {__name__} successfully on URL: {url}")
            time.sleep(15)


if __name__ == "__main__":
    if internet_on():
        os.chdir(r"C:\Users\hp\Scripts\miniprograms\Amazon Product Price")
        logger = log_config()
        main()
