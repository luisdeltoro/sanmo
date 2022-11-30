from datetime import datetime
import json
from pathlib import Path

from sanmo.model import Dimension, Metric
from sanmo.util import (
    convert_to_metrics,
    remove_prefix_if_exists,
    remove_suffix_if_exists,
    reshape,
)


def test_reshape() -> None:
    timestamp = datetime.strptime("2022-11-30_20:13:01", "%Y-%m-%d_%H:%M:%S")
    input_as_str = Path("tests/ships_example.json").read_text()
    expected_as_str = Path("tests/ships_expected.json").read_text()
    input = json.loads(input_as_str)
    expected = json.loads(expected_as_str)

    result = reshape(timestamp, input)
    print(result)
    assert result == expected


def test_remove_prefix_if_exists() -> None:
    input = "sanmo_store/2022-11-30_20:13:01.json"
    expected = "2022-11-30_20:13:01.json"

    result = remove_prefix_if_exists(input, "/")
    assert result == expected


def test_remove_suffix_if_exists() -> None:
    input = "sanmo_store/2022-11-30_20:13:01.json"
    expected = "sanmo_store/2022-11-30_20:13:01"

    result = remove_suffix_if_exists(input, ".json")
    assert result == expected


def test_convert_to_metrics() -> None:
    ships_reshaped = [
        {
            "name": "VZUS opod",
            "timestamp": "2022-11-30_20:13:01",
            "vwap": 1666.67,
            "class": "medium",
            "rarity": "rare",
            "totalSupply": 1900,
            "tradingInUsdc": {
                "highestBid": 511,
                "lowestAsk": 533,
                "buyOrderNum": 12,
                "sellOrderNum": 7,
                "priceVsVwapPercentage": -68.68,
            },
            "tradingInAtlas": {
                "highestBid": 12010,
                "highestBidConvertedToUsdc": 33.2677554,
                "lowestAsk": 218000,
                "lowestAskConvertedToUsdc": 603.86,
                "buyOrderNum": 23,
                "sellOrderNum": 1,
                "priceVsVwapPercentage": -80.89,
            },
        },
        {
            "name": "Calico Guardian",
            "timestamp": "2022-11-30_20:13:01",
            "vwap": 30883.91,
            "class": "capital",
            "rarity": "legendary",
            "totalSupply": 235,
            "tradingInUsdc": {
                "highestBid": 5200,
                "lowestAsk": 6500,
                "buyOrderNum": 8,
                "sellOrderNum": 2,
                "priceVsVwapPercentage": -81.06,
            },
            "tradingInAtlas": {
                "highestBid": 100000,
                "highestBidConvertedToUsdc": 277,
                "buyOrderNum": 17,
                "sellOrderNum": 0,
                "priceVsVwapPercentage": -99.1,
            },
        },
    ]
    expected = [
        Metric(
            "StarAtlas",
            "VZUS opod (medium - rare) | 1666.67 | 1900",
            datetime(2022, 11, 30, 20, 13, 1),
            533,
            [Dimension("price-type", "lowestAsk"), Dimension("category", "tradingInUsdc")],
        ),
        Metric(
            "StarAtlas",
            "VZUS opod (medium - rare) | 1666.67 | 1900",
            datetime(2022, 11, 30, 20, 13, 1),
            603.86,
            [
                Dimension("price-type", "lowestAskConvertedToUsdc"),
                Dimension("category", "tradingInAtlas"),
            ],
        ),
        Metric(
            "StarAtlas",
            "Calico Guardian (capital - legendary) | 30883.91 | 235",
            datetime(2022, 11, 30, 20, 13, 1),
            6500,
            dimensions=[
                Dimension("price-type", "lowestAsk"),
                Dimension("category", "tradingInUsdc"),
            ],
        ),
    ]

    result = convert_to_metrics(
        ships_reshaped,
        [
            ("tradingInUsdc", "lowestAsk", "None"),
            ("tradingInAtlas", "lowestAskConvertedToUsdc", "None"),
        ],
    )
    print(result)
    assert result == expected
