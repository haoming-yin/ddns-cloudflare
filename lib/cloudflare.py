""" A cloudflare related help module"""

import os
import re

import requests

from .error import *

API_URL = "https://api.cloudflare.com/client/v4"


def _validate_record_type(record_type: str, check=True):
    """ Validates record type.
    Args:
        record_type: record type
        check: set true to throw error when the given record type is invalid.
    Returns:
        boolean: True if the record type is valid
    """
    valid_types = ["A", "AAAA", "CNAME", "TXT", "SRV", "LOC", "MX", "NS", "SPF", "CERT", "DNSKKEY",
                   "DS", "NAPTR", "SMIMEA", "SSHFP", "TLSA", "URI"]
    if check and record_type not in valid_types:
        raise CloudflareAPIError(f"DNS record type '{record_type}' is invalid.")

    if record_type == "MX":
        # you can have multiple MX records with different content
        # TODO: should duplicated MX records be removed first???
        raise CloudflareAPIError("We don't support 'MX' records yet, as it could have multiple values")

    return record_type in valid_types


def _get_headers():
    email = os.getenv("X_AUTH_EMAIL")
    token = os.getenv("X_AUTH_KEY")
    if not email or not token:
        raise CloudflareError("Cannot find API credential - X_AUTH_EMAIL or/and X_AUTH_KEY in environment")

    return {
        "X-Auth-Key": token,
        "X-Auth-Email": email
    }


def _get(endpoint, **kwargs):
    res = requests.get(f"{API_URL}/{endpoint}", headers=_get_headers(), **kwargs).json()
    if res["success"]:
        return res["result"]
    raise CloudflareAPIError("Cloudflare API error", extra=dict(endpoint=endpoint, errors=res["errors"]))


def _put(endpoint, **kwargs):
    res = requests.put(f"{API_URL}/{endpoint}", headers=_get_headers(), **kwargs).json()
    if res["success"]:
        return res["result"]
    raise CloudflareAPIError("Cloudflare API error", extra=dict(endpoint=endpoint, errors=res["errors"]))


def _post(endpoint, **kwargs):
    res = requests.post(f"{API_URL}/{endpoint}", headers=_get_headers(), **kwargs).json()
    if res["success"]:
        return res["result"]
    raise CloudflareAPIError("Cloudflare API error", extra=dict(endpoint=endpoint, errors=res["errors"]))


def get_zone(*, zone_name: str):
    """ Get zone with given zone name.
    Args:
        zone_name: zone name, e.g. "haomingyin.com"
    Returns:
        json: zone details
    """
    params = dict(name=zone_name)
    zones = _get("zones", params=params)
    if not zones:
        raise CloudflareAPIError(f"Unable to fetch zone {zone_name}")
    return zones[0]


def get_dns_records(*, zone_name: str, record_type: str, name: str, content: str = None):
    """ Get DNS records with given record properties.
    Args:
        zone_name: zone name.
        record_type: dns record type.
        name: dns record name. Notes: name has to have zone name included;
        content: dns record content.
    Returns:
        List: a list of json records.
    """
    params = {}
    if record_type:
        _validate_record_type(record_type, check=True)
        params["type"] = record_type
    if name:
        params["name"] = name
        if name != zone_name and not re.match(rf".*\.{zone_name}", name):
            params["name"] = f"{name}.{zone_name}"
    if content:
        params["content"] = content

    zone_id = get_zone(zone_name=zone_name)["id"]
    return _get(f"zones/{zone_id}/dns_records", params=params)


def set_dns_record(*, zone_name: str, record_type: str, name: str, content: str, ttl=1, proxied=False):
    """ Create a DNS record if it's not existed, otherwise update the existing one.
    Args:
        zone_name: zone name.
        record_type: dns record type.
        name: record name.
        content: content that to be updated.
        ttl: time to live, default to 2 minutes.
        proxied: if the DNS is proxied by cloudflare.
    """
    _validate_record_type(record_type, check=True)

    records = get_dns_records(zone_name=zone_name, record_type=record_type, name=name)

    data = dict(type=record_type, name=name, content=content, ttl=ttl, proxied=proxied)
    zone_id = get_zone(zone_name=zone_name)["id"]

    if records:
        record_id = records[0]["id"]
        return _put(f"zones/{zone_id}/dns_records/{record_id}", json=data)
    return _post(f"zones/{zone_id}/dns_records", json=data)
