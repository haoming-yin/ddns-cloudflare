""" Invoke collection -- cloudflare """

import yaml
from invoke import Collection, task
from helper import cloudflare, ip, logger

LOG = logger.get_logger()


def load_config(file_path="./config.yml"):
    """ Load config file"""
    print(f"Loading config file '{file_path}' ...")
    with open(file_path, "r") as file:
        return yaml.load(file)


@task
def sync_record(_, zone_name, record_type, name, content=None, ttl=1):
    """ Sync a DNS record"""
    if content is None:
        content = ip.get_public_ip()

    params = dict(zone_name=zone_name, record_type=record_type, name=name, content=content)
    if cloudflare.get_dns_records(**params):  # if a record's content is not identical in cloud
        print(f"Not need to sync - [{record_type}] {name}: {content} - is identical in cloud")
    else:
        print(f"Start sync - [{record_type}] {name}: {content}")
        if cloudflare.set_dns_record(**params, ttl=ttl):
            print(f"Sync completed - [{record_type}] {name}: {content}")
        else:
            print(f"Sync failed - [{record_type}] {name}: {content}")


@task(default=True)
def sync(ctx):
    """ Sync DNS records"""
    records = load_config()["records"]
    print("Config file has been loaded")

    for record in records:
        try:
            zone_name = record["zone_name"]
            record_type = record["record_type"]
            name = record["name"]
            content = record.get("content")
            ttl = record.get("ttl", 1)
            sync_record(ctx, zone_name, record_type, name, content, ttl)
        except KeyError as err:
            print(f"Record in config.yml must contain: [zone_name, record_type, name] - {err}")


namespace = Collection("cf")  # pylint: disable=invalid-name
namespace.add_task(sync)
namespace.add_task(sync_record)
