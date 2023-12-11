"""
This module contains a script that automates the export of a PDF document from an Overleaf project.
The script uses the `playwright` library to control a Chromium browser instance, navigate to the
specified Overleaf URL, and initiate the download of the project's output PDF.

The Overleaf project is accessed via a read-only share link, which should be provided through the
`OVERLEAF_URL` environment variable. The downloaded PDF is saved to the current working directory
with the filename 'document.pdf'.

Environment Variables:
    - OVERLEAF_URL
        A string containing the Overleaf read-only share link used to access the project.

Example Usage:
    Invoke the script by setting the `OVERLEAF_URL` environment variable to the read-only share link
    and running the script. For example:

    .. code-block:: bash

        $ export OVERLEAF_URL=https://www.overleaf.com/read/hbduvlpfoewj#5e625c
        $ python src/main.py

"""

import os
import tempfile
from typing import Tuple

from playwright.sync_api import sync_playwright

from config import *

RENDER_TIMEOUT = 61_000
URL = os.getenv("OVERLEAF_URL")

logging.basicConfig(**LOGGING_BASIC_CONFIG)


def get_document_bytes(overleaf_url: str) -> Tuple[str, bytes]:
    """
    Retrieves the PDF document from an Overleaf project as a bytes object.

    This function automates the process of downloading the output PDF from an Overleaf project using a headless
    Chromium browser instance. It navigates to the given Overleaf URL, waits for the project's canvas to load,
    and then triggers the download by clicking the appropriate button.

    Args:
        overleaf_url (str): The URL of the Overleaf project from which to download the PDF.

    Returns:
        str: The filename of the downloaded PDF.
        bytes: The content of the PDF document in bytes.

    Note:
        The Overleaf URL should be a read-only share link to ensure that the document can be accessed without
        needing to log in, and that it cannot be accidentally modified.
    """
    with sync_playwright() as p:
        logging.info("Launching Chromium browser instance")
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        logging.info("Navigating to Overleaf URL %s", overleaf_url)
        page.goto(overleaf_url)
        canvas_xpath = """//div[@class='canvasWrapper']"""
        logging.info(
            "Waiting for canvas to load (i.e. for the LaTeX to render). This may take a while..."
        )
        page.set_default_timeout(RENDER_TIMEOUT)
        page.wait_for_selector(canvas_xpath)
        download_button_xpath = r"//i[contains(@class, 'fa-download')]"
        with page.expect_download() as download_info:
            logging.info("Clicking download button")
            page.click(download_button_xpath)
        download = download_info.value
        with tempfile.TemporaryDirectory() as download_buffer:
            path = os.path.join(download_buffer, download.suggested_filename)
            logging.info("Saving PDF to %s", path)
            download.save_as(path)
            browser.close()
            with open(path, "rb") as downloaded_file:
                document_bytes = downloaded_file.read()
    logging.info(
        "Successfully retrieved PDF document '%s' of size %d bytes",
        download.suggested_filename,
        len(document_bytes),
    )
    return download.suggested_filename, document_bytes


if __name__ == "__main__":
    document_name, downloaded_document = get_document_bytes(overleaf_url=URL)
    with open("document.pdf", "wb") as debug_output_file:
        debug_output_file.write(downloaded_document)
