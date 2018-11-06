""" Logger module"""

import os
from logging import Logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOGGER = Logger("cloudflare", LOG_LEVEL)


def get_logger():
    """ Gets the logger"""
    return LOGGER
