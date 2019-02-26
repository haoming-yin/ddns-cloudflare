""" IP related functions"""

import requests
from helper import logger

LOG = logger.get_logger()


def get_public_ip():
    """ Get IP address of the machine that running this function"""
    try:
        res = requests.get("https://api.ipify.org")
        if res.status_code in [200, 201]:
            return res.text
        raise Exception(f"Status code is {res.status_code}")
    except Exception as err:
        LOG.exception(f"Failed to fetch local machine public IP - {err}")
        return None
