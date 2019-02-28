import os
import time
from subprocess import run

from lib.utilities import load_config

profile = os.getenv("DDNS_PROFILE", "default")
interval = load_config(profile=profile).get("interval", 0)

while True:
    run(["inv", "cf.sync", f"--profile={profile}"], check=False)
    if interval == 0:
        break
    time.sleep(interval)
