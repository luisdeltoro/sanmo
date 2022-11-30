from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sanmo.model import Dimension, Metric


def reshape(timestamp: datetime, ships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pruned_input = [
        {
            "name": x["name"],
            "timestamp": timestamp.strftime("%Y-%m-%d_%H:%M:%S"),
            "vwap": x["vwap"],
            "class": x["class"],
            "rarity": x["rarity"],
            "totalSupply": x["totalSupply"],
            "tradingInUsdc": {
                "highestBid": x["pricing"].get("highestBid"),
                "lowestAsk": x["pricing"].get("lowestAsk"),
                "buyOrderNum": x["pricing"].get("buyOrderNum"),
                "sellOrderNum": x["pricing"].get("sellOrderNum"),
                "priceVsVwapPercentage": x["pricing"].get("percentageFromVWAP"),
            },
            "tradingInAtlas": {
                "highestBid": x["pricingATL"].get("highestBidATL"),
                "highestBidConvertedToUsdc": x["pricingATL"].get("highestBid"),
                "lowestAsk": x["pricingATL"].get("lowestAskATL"),
                "lowestAskConvertedToUsdc": x["pricingATL"].get("lowestAsk"),
                "buyOrderNum": x["pricingATL"].get("buyOrderNum"),
                "sellOrderNum": x["pricingATL"].get("sellOrderNum"),
                "priceVsVwapPercentage": x["pricingATL"].get("percentageFromVWAP"),
            },
        }
        for x in ships
    ]
    return pruned_input


def remove_prefix_if_exists(name: str, separator: str = "/") -> str:
    first_slash_index = name.find(separator)
    if first_slash_index != -1:
        return name[first_slash_index + 1 :]
    else:
        return name


def remove_suffix_if_exists(name: str, suffix: str = ".json") -> str:
    if name.endswith(suffix):
        return name[: -(len(suffix))]
    else:
        return name


def convert_to_metrics(
    reshaped_ships: List[Dict[str, Any]], fields: List[Tuple[str, str, str]]
) -> List[Metric]:
    new_ships = []
    for ship in reshaped_ships:
        for category, field, unit in fields:
            metric = convert_ship_field_to_metric(ship, category, field, unit)
            if metric:
                new_ships.append(metric)
    return new_ships


def convert_ship_field_to_metric(
    ship: Dict[str, Any], field_ns: str, field: str, unit: str = "None"
) -> Optional[Metric]:
    value = ship[field_ns].get(field)
    if value:
        return Metric(
            "StarAtlas",
            f"{ship['name']} ({ship['class']} - {ship['rarity']}) | {ship['vwap']} | {ship['totalSupply']}",
            datetime.strptime(ship["timestamp"], "%Y-%m-%d_%H:%M:%S"),
            value,
            [Dimension("price-type", field), Dimension("category", field_ns)],
            unit,
        )
    else:
        return None
