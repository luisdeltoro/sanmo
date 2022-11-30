from datetime import datetime
import json
import os

import requests

from sanmo.local_filesystem_storage import store as store_in_local_fs
from sanmo.s3_storage import store as store_in_s3
from sanmo.util import reshape

aephie_ships_url = "https://get-ship-data.aephia.workers.dev/gm/ships"


def lambda_handler(event, context):
    ships_str = fetch_ships()
    now = datetime.now()
    print(ships_str)
    ships = json.loads(ships_str)
    store_in_s3("sanmo_store", now, ships)
    pruned_ships = reshape(now, ships)
    return pruned_ships


def main() -> None:
    store_dir = os.environ["HOME"] + "/sanmo_store"
    ships_str = fetch_ships()
    ships = json.loads(ships_str)

    now = datetime.now()
    pruned_ships = reshape(now, ships)
    pruned_ships_str_formatted = json.dumps(pruned_ships, indent=2)

    print(pruned_ships_str_formatted)
    store_in_local_fs(store_dir, now, ships)


def fetch_ships() -> str:
    response = requests.get(aephie_ships_url)
    return response.content.decode()


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    main()
