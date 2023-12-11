"""
This module provides functionality to automate the process of uploading documents to a SharePoint site.
It utilizes the Playwright library to interact with web pages, simulating a user logging in to SharePoint with credentials
and uploading a file.

The main function `upload_document_to_sharepoint` takes in file information and user credentials, handles the login process if necessary,
and uploads the file to the specified SharePoint URL. It uses a helper function `log_in` to perform the actual login steps.

A cookie file is used to store and reuse login session information to avoid logging in multiple times.
The Playwright browser context is set to headless mode by default, meaning it runs in the background without opening a visible window.

Functions:
- upload_document_to_sharepoint: Automates the document upload process to SharePoint.
- log_in: Helper function to perform the login action on a Microsoft account page.

Usage:
To use this module, set the required environment variables for SharePoint URL, username, and password.
The document to be uploaded should be specified as a file name and its byte content.
"""

import json
import os
from tempfile import TemporaryDirectory
from time import time

from playwright.sync_api import sync_playwright

from config import *

logging.basicConfig(**LOGGING_BASIC_CONFIG)

URL = os.getenv("SHAREPOINT_URL")
USERNAME = os.getenv("MICROSOFT_USERNAME")
PASSWORD = os.getenv("MICROSOFT_PASSWORD")
COOKIES_FILE = os.getenv("COOKIES_FILE")


def upload_document_to_sharepoint(
    file_name: str, file_bytes: bytes, sharepoint_url: str, username: str, password: str
) -> None:
    """
    Uploads a document to SharePoint using provided credentials.

    This function automates the process of logging into SharePoint and uploading a document using Playwright.
    It checks if the login page is present, and if so, it will log in using the provided credentials.
    Then it uploads the file by creating a temporary file from the provided bytes and handling the file chooser.

    :param file_name: The name of the file to be uploaded.
    :param file_bytes: The binary content of the file to be uploaded.
    :param sharepoint_url: The URL of the SharePoint site where the document will be uploaded.
    :param username: The username (usually an email) for logging into SharePoint.
    :param password: The password associated with the username for logging into SharePoint.
    :return: None. The function performs actions but does not return any value.
    """
    with open(COOKIES_FILE, "r") as cookies_file:
        logging.info("Loading cookies from file")
        cookies = json.load(cookies_file)
        logging.info("Loaded %d cookies", len(cookies))

    with sync_playwright() as p:
        logging.info("Launching Chromium browser instance")
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        logging.info("Setting cookies")
        context.add_cookies(cookies)
        page = context.new_page()
        logging.info("Navigating to SharePoint URL %s", sharepoint_url)
        page.goto(sharepoint_url)
        if (
            page.query_selector("""//input[@type='password']""") is not None
            or page.query_selector("""//input[@type='email']""") is not None
        ):
            log_in(page, password, username)
        page.click("""//i[@data-icon-name='upload']""")
        with TemporaryDirectory() as upload_buffer:
            new_file_name = file_name.replace(".pdf", f"-{int(time())}.pdf")
            path = os.path.join(upload_buffer, new_file_name)
            with open(path, "wb") as upload_file:
                upload_file.write(file_bytes)
            logging.info("Uploading file %s", path)
            with page.expect_file_chooser() as fc_info:
                page.click(
                    """//li[@role='presentation']//span[contains(text(),'Files')]"""
                )
            file_chooser = fc_info.value
            file_chooser.set_files(path)

        page.wait_for_selector("""//div[contains(text(),'Uploaded')]""")
        logging.info("File uploaded successfully")
        logging.info("Saving cookies to file")
        with open(COOKIES_FILE, "w") as cookies_file:
            json.dump(page.context.cookies(), cookies_file)
            logging.info("Saved %d cookies", len(page.context.cookies()))
        logging.info("Closing browser")
        browser.close()


def log_in(page, password: str, username: str):
    """
    Performs login action on a Microsoft account within a Playwright page.

    The function fills in the username and password on the login form, and submits the form to log into the account.
    It is intended to be used for automation tasks where a Microsoft login is required, such as interacting with SharePoint.

    :param page: The Playwright page object in which the login interaction takes place.
    :param username: The username (usually an email) for the Microsoft account.
    :param password: The password for the Microsoft account.
    :return: None. The function performs actions but does not return any value.
    """
    if page.query_selector("""//input[@type='email']""") is None:
        page.fill("""//input[@type='email']""", username)
        page.click("""//input[@type='submit']""")
    if page.query_selector("""//input[@type='password']""") is None:
        page.fill("""//input[@type='password']""", password)
        page.click("""//input[@type='submit']""")
    ...
    # save cookies
    with open(COOKIES_FILE, "w") as cookies_file:
        logging.info("Saving cookies to file")
        json.dump(page.context.cookies(), cookies_file)
        logging.info("Saved %d cookies", len(page.context.cookies()))


if __name__ == "__main__":
    filename = str()
    document_bytes = bytes()
    upload_document_to_sharepoint(filename, document_bytes, URL, USERNAME, PASSWORD)
