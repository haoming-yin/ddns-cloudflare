""" IP related functions"""

import requests

from .error import *


def get_public_ip():
    """ Get IP address of the machine that running this function"""
    res = requests.get("https://api.ipify.org")
    if res.status_code in [200, 201]:
        return res.text
    raise CloudflareIPError("Failed to fetch public IP", extra=dict(response=res.text, status_code=res.status_code))
