""" A cloudflare related help module"""

import os
import json
import CloudFlare
from helper import logger

LOG = logger.get_logger()


def _validate_record_type(record_type):
    """ Return True if record_type is valid"""
    valid_types = ["A", "AAAA", "CNAME", "TXT", "SRV", "LOC", "MX", "NS", "SPF", "CERT", "DNSKKEY",
                   "DS", "NAPTR", "SMIMEA", "SSHFP", "TLSA", "URI"]
    return record_type in valid_types


def _get_client():
    """ Get Cloudflare client with auth credentials passed in"""
    email = os.getenv("X_AUTH_EMAIL")
    token = os.getenv("X_AUTH_KEY")
    if not email or not token:
        LOG.error(
            "Cannot find API credential - X_AUTH_EMAIL or/and X_AUTH_KEY in environment")
    else:
        return CloudFlare.CloudFlare(email, token)


def get_zone(*, zone_name):
    """ Get zone id with given name"""
    client = _get_client()

    try:
        params = {"name": zone_name}
        zones = client.zones.get(params=params)
        LOG.debug(f"[GET] zones")
    except Exception as err:
        LOG.error(f"[GET] zones - ${err} - api call failed")
        return

    if len(zones) != 1:
        LOG.error(
            f"[GET] zones - should get only one zone, but got ${len(zones)}")
        return

    return zones[0]


def get_dns_records(*, zone_name=None, zone_id=None, record_type=None, name=None, content=None):
    """ Get DNS record is with given record properties"""
    client = _get_client()
    zone_id = zone_id if zone_id else get_zone(zone_name=zone_name)["id"]
    assert zone_id is not None

    try:
        params = {}
        if record_type:
            if not _validate_record_type(record_type):
                raise TypeError(f"DNS record type '${record_type} is invalid.")
            params["type"] = record_type
        if name:
            params["name"] = name
        if content:
            params["content"] = content

        LOG.debug(f"[GET] zones/{zone_id}/dns_records")
        records = client.zones.dns_records.get(params=params, identifier1=zone_id)
    except Exception as err:
        LOG.error(f"[GET] zones/{zone_id}/dns_records - ${err} - api call failed")
        return

    return records


def set_dns_record(*, zone_name=None, zone_id=None, record_type, name, content, ttl=1, priority=10):
    """ Create a DNS record if it's not existed, otherwise update the existing one"""
    client = _get_client()
    zone_id = zone_id if zone_id else get_zone(zone_name=zone_name)["id"]
    assert zone_id is not None

    if not _validate_record_type(record_type):
        LOG.error(f"DNS record type '${record_type} is invalid.")
    data = {"type": record_type, "name": name}

    if record_type == "MX":
        # you can have multiple MX records with different content
        # TODO: should duplicated MX records be removed first???
        raise TypeError(f"We don't support 'MX' records yet, as it could have multiple values")

    records = get_dns_records(zone_id=zone_id, record_type=record_type, name=name)
    data["content"] = content
    data["ttl"] = ttl

    if len(records) > 0:
        try:
            res = client.zones.dns_records.put(
                identifier1=zone_id, identifier2=records[0]["id"], data=data)
        except Exception as err:
            LOG.error(
                f"[PUT] zones/{zone_id}/dns_records/{records[0]['id']} - ${err} - api call failed")
    else:
        try:
            res = client.zones.dns_records.post(identifier1=zone_id, data=data)
        except Exception as err:
            LOG.error(f"[POST] zones/{zone_id}/dns_records/- ${err} - api call failed")

    print(res)
