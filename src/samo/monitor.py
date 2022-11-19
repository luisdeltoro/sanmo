import json
from pathlib import Path
from typing import Any, Dict, List

url = "https://get-ship-data.aephia.workers.dev/gm/ships"


def main() -> None:
    ships_str = Path("ships.json").read_text()
    ships = json.loads(ships_str)

    ships_str_formatted = json.dumps(ships, indent=2)
    pruned_ships = prune_non_relevant_fields(ships)
    pruned_ships_str_formatted = json.dumps(pruned_ships, indent=2)

    print(ships_str_formatted)
    print(pruned_ships_str_formatted)


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
