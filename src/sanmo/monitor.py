import json
import os
from typing import Any, Dict, List

import requests

# from local_filesystem_storage import store
from s3_storage import store

aephie_ships_url = "https://get-ship-data.aephia.workers.dev/gm/ships"


def lambda_handler(event, context):
    ships_str = fetch_ships()
    print(ships_str)
    ships = json.loads(ships_str)
    pruned_ships = prune_non_relevant_fields(ships)
    return pruned_ships


def main() -> None:
    store_dir = os.environ["HOME"] + "/sanmo_store"
    ships_str = fetch_ships()
    ships = json.loads(ships_str)

    pruned_ships = prune_non_relevant_fields(ships)
    pruned_ships_str_formatted = json.dumps(pruned_ships, indent=2)

    print(pruned_ships_str_formatted)
    store(store_dir, ships)


def fetch_ships() -> str:
    response = requests.get(aephie_ships_url)
    return response.content.decode()


def prune_non_relevant_fields(input: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pruned_input = [
        {
            "name": x["name"],
            "vwap": x["vwap"],
            "originationPrice": x["originationPrice"],
            "bestAsk": x["pricing"].get("lowestAsk"),
            "askVsVwap": x["pricing"].get("percentageFromVWAPAsk"),
        }
        for x in input
    ]
    return pruned_input


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    main()
