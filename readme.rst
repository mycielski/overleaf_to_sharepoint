PDF Export Automation Script
=============================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Overview
--------

This module provides an automation script for exporting PDF documents from Overleaf projects.
It uses the `playwright` library to automate a Chromium browser instance, allowing users to
navigate to their Overleaf project and download the PDF output.

The script requires a read-only share link from Overleaf, which should be provided via the
`OVERLEAF_URL` environment variable. The script will save the downloaded PDF as 'document.pdf'
in the current working directory.

Prerequisites
-------------

Ensure you have all the necessary requirements installed.
You can install all required packages using:

.. code-block:: bash

    $ pip install -r requirements.txt

Environment Variables
---------------------

- `OVERLEAF_URL`: The Overleaf read-only share link. Example: `https://www.overleaf.com/read/hbduvlpfoewj#5e625c`

Usage
-----

To use the script, set the `OVERLEAF_URL` environment variable to your Overleaf read-only share link,
and then execute the script:

.. code-block:: bash

    $ export OVERLEAF_URL=<your_overleaf_read_only_link>
    $ python src/main.py
