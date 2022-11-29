from datetime import datetime
import json
import os
from typing import Any, Dict, List

import requests

from sanmo.local_filesystem_storage import store as store_in_local_fs
from sanmo.s3_storage import store as store_in_s3

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


def reshape(
    timestamp: datetime, ships: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    pruned_input = [
        {
            "name": x["name"],
            "timestamp": timestamp.strftime("%Y-%m-%d_%H:%M:%S"),
            "vwap": x["vwap"],
            "class": x["class"],
            "rarity": x["rarity"],
            "totalSupply": x["totalSupply"],
            "currentPricingInUsdc": {
                "highestBid": x["pricing"].get("highestBid"),
                "lowestAsk": x["pricing"].get("lowestAsk"),
                "buyOrderNum": x["pricing"].get("buyOrderNum"),
                "sellOrderNum": x["pricing"].get("sellOrderNum"),
                "priceVsVwapPercentage": x["pricing"].get("percentageFromVWAP"),
            },
            "currentPricingInAtlas": {
                "highestBid": x["pricingATL"].get("highestBidATL"),
                "highestBidConvertedToUsdc": x["pricingATL"].get("highestBid"),
                "lowestAsk": x["pricingATL"].get("lowestAskATL"),
                "lowestAskConvertedToUsdc": x["pricingATL"].get("lowestAsk"),
                "buyOrderNum": x["pricingATL"].get("buyOrderNum"),
                "sellOrderNum": x["pricingATL"].get("sellOrderNum"),
                "priceVsVwapPercentage": x["pricingATL"].get("percentageFromVWAP"),
            }
        }
        for x in ships
    ]
    return pruned_input


# Allow the script to be run standalone (useful during development).
if __name__ == "__main__":
    main()
