"""
This script coordinates the retrieval of a document from Overleaf and its subsequent upload to SharePoint.
It uses the configurations specified in 'config.py' for logging and environment variables to handle credentials and URLs.
The `main` function orchestrates the process, logging each major step.
"""

import logging
import os

from config import LOGGING_BASIC_CONFIG
from overleaf import get_document_bytes
from sharepoint import upload_document_to_sharepoint

logging.basicConfig(**LOGGING_BASIC_CONFIG)


def main():
    """
    Main function to download a document from Overleaf and upload it to SharePoint.

    It retrieves the document from Overleaf using the URL from environment variables,
    logs the process, and then uploads the document to SharePoint with the credentials
    and URL also specified in the environment variables.
    """
    logging.info("---OVERLEAF STARTING---")
    name, content = get_document_bytes(os.getenv("OVERLEAF_URL"))
    logging.info("---OVERLEAF FINISHED---")

    logging.info("---SHAREPOINT STARTING---")
    upload_document_to_sharepoint(
        file_name=name,
        file_bytes=content,
        sharepoint_url=os.getenv("SHAREPOINT_URL"),
        username=os.getenv("MICROSOFT_USERNAME"),
        password=os.getenv("MICROSOFT_PASSWORD"),
    )
    logging.info("---SHAREPOINT FINISHED---")


if __name__ == "__main__":
    main()
