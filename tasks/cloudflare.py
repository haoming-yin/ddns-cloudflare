""" Invoke collection -- cloudflare """

import sys

from invoke import Collection, task

from lib import cloudflare, ip, utilities, error


@task
def sync_record(_, zone_name, record_type, name, content=None, ttl=1, proxied=False):
    """ Sync a DNS record"""
    try:
        if content is None:
            content = ip.get_public_ip()
        record_meta = f"[{record_type}] {name}: {content}"

        if content is None:
            print(f"Failed to fetch local machine public IP. Skip - {record_meta}")
            return

        params = dict(zone_name=zone_name, record_type=record_type, name=name, content=content)
        records = cloudflare.get_dns_records(**params)
        if records and records[0]["proxied"] == proxied: # if a record's content is not identical in cloud
            print(f"Not need to sync - {record_meta} - is identical with Cloudflare")
        else:
            print(f"Start sync - {record_meta}")
            if cloudflare.set_dns_record(**params, ttl=ttl, proxied=proxied):
                print(f"Sync completed - {record_meta}")
            else:
                print(f"Sync failed - {record_meta}")
    except error.CloudflareError as err:
        print(f"ERROR: {str(err)} -- {err.extra}", file=sys.stderr)
        exit(1)
    except Exception as err:
        print(f"ERROR: {str(err)}", file=sys.stderr)
        exit(1)


@task(default=True)
def sync(ctx, config_path="./config.yml", profile="default"):
    """ Sync DNS records"""
    try:
        print(f"Loading config file '{config_path}' ...")
        records = utilities.load_config(file_path=config_path, profile=profile).get("records", [])
        print("Config file has been loaded")

        for record in records:
            try:
                zone_name = record["zone_name"]
                record_type = record["record_type"]
                name = record["name"]
                content = record.get("content")
                ttl = record.get("ttl", 1)
                proxied = record.get("proxied", False)
                sync_record(ctx, zone_name, record_type, name, content, ttl, proxied)
            except KeyError as err:
                print(f"Record in config.yml must contain: [zone_name, record_type, name] - {err}")
    except error.CloudflareError as err:
        print(f"ERROR: {str(err)} -- {err.extra}", file=sys.stderr)
        exit(1)
    except Exception as err:
        print(f"ERROR: {str(err)}", file=sys.stderr)
        exit(1)


namespace = Collection("cf")  # pylint: disable=invalid-name
namespace.add_task(sync)
namespace.add_task(sync_record)
