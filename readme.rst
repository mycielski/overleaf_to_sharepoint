==============================
 Overleaf to SharePoint Export
==============================

Overview
========

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

This Python project automates the retrieval of PDF documents from Overleaf and uploads them to a SharePoint site. It leverages the `playwright` library to interact with web pages programmatically.

The project consists of a set of modules in the `src` directory:
- `config.py`: Contains configuration for logging and headless browser mode.
- `overleaf.py`: Handles the export of a PDF from an Overleaf project.
- `sharepoint.py`: Automates the uploading of documents to SharePoint.
- `main.py`: Coordinates the entire process from retrieval to upload.

Requirements
============

- Python 3.x
- Playwright library
- Environment variables set for Overleaf and SharePoint URLs, and Microsoft account credentials.

Installation
============

Clone the repository and navigate to the project directory:

.. code-block:: bash

    git clone [repository-url]
    cd [project-directory]

Install dependencies:

.. code-block:: bash

    pip install -r requirements.txt

Usage
=====

Set the necessary environment variables:

.. code-block:: bash

    export OVERLEAF_URL=[overleaf-read-only-share-link]
    export SHAREPOINT_URL=[sharepoint-site-url]
    export MICROSOFT_USERNAME=[your-email]
    export MICROSOFT_PASSWORD=[your-password]
    export COOKIES_FILE=[path-to-cookies-file]

Run the main script:

.. code-block:: bash

    python src/main.py

Documentation
=============

Each module contains a docstring describing its purpose and usage. Please refer to the module files for detailed information on each part of the project.
