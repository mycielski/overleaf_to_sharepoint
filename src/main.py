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

from playwright.sync_api import sync_playwright

OVERLEAF_URL = os.getenv("OVERLEAF_URL")


def get_document_bytes(overleaf_url: str) -> bytes:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(overleaf_url)
        canvas_xpath = """//div[@class='canvasWrapper']"""
        page.wait_for_selector(canvas_xpath)
        download_button_xpath = r"//i[contains(@class, 'fa-download')]"
        with page.expect_download() as download_info:
            page.click(download_button_xpath)
        download = download_info.value
        with tempfile.TemporaryDirectory() as download_buffer:
            path = os.path.join(download_buffer, download.suggested_filename)
            download.save_as(path)
            browser.close()
            with open(path, "rb") as f:
                document_bytes = f.read()

    return document_bytes


def main() -> None:
    """
    Main function. No arguments but takes the Overleaf read-only
    share link provided as `OVERLEAF_URL` environment variable.
    """
    get_document_bytes(overleaf_url=OVERLEAF_URL)


if __name__ == "__main__":
    main()
