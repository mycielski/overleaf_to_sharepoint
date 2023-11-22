"""
This file contains the configuration for the application.

Attributes:
- LOGGING_BASIC_CONFIG (dict): A dictionary containing the basic configuration for logging,
  including the logging level and the format for log messages.
- HEADLESS (bool): A boolean flag to control whether the browser should run in headless mode.
"""

import logging

LOGGING_BASIC_CONFIG = {
    "level": logging.INFO,
    "format": "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s",
}
HEADLESS = False
