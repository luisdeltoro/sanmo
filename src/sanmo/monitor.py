from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

aephie_ships_url = "https://get-ship-data.aephia.workers.dev/gm/ships"
store_dir = os.environ["HOME"] + "/samo_store"


def lambda_handler(event, context):
    ships_str = fetch_ships()
    ships = json.loads(ships_str)
    pruned_ships = prune_non_relevant_fields(ships)
    return pruned_ships


def main() -> None:
    ships_str = fetch_ships()
    ships = json.loads(ships_str)

    pruned_ships = prune_non_relevant_fields(ships)
    pruned_ships_str_formatted = json.dumps(pruned_ships, indent=2)

    print(pruned_ships_str_formatted)
    store(pruned_ships)


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


def store(ships_price_info: List[Dict[str, Optional[str]]]) -> None:
    now = datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H:%M:%S.json")
    Path(store_dir + "/" + file_name).write_text(json.dumps(ships_price_info))


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    main()
