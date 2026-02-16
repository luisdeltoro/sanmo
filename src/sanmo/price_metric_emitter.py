from datetime import datetime
import json
import urllib.parse

import boto3
from botocore.config import Config

from sanmo.cloud_watch_metrics import emit_metric
from sanmo.util import (
    convert_to_metrics,
    remove_prefix_if_exists,
    remove_suffix_if_exists,
    reshape,
)

config = Config(region_name="us-east-1")
cw = boto3.client("cloudwatch", config=config)
s3 = boto3.client("s3", config=config)

fields = [
    ("tradingInUsdc", "highestBid", "None"),
    ("tradingInUsdc", "lowestAsk", "None"),
    ("tradingInUsdc", "buyOrderNum", "Count"),
    ("tradingInUsdc", "sellOrderNum", "Count"),
    ("tradingInUsdc", "priceVsVwapPercentage", "Percent"),
    ("tradingInAtlas", "highestBid", "None"),
    ("tradingInAtlas", "highestBidConvertedToUsdc", "None"),
    ("tradingInAtlas", "lowestAsk", "None"),
    ("tradingInAtlas", "lowestAskConvertedToUsdc", "None"),
    ("tradingInAtlas", "buyOrderNum", "Count"),
    ("tradingInAtlas", "sellOrderNum", "Count"),
    ("tradingInAtlas", "priceVsVwapPercentage", "Percent"),
]


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    try:
        response = s3.get_object(
            Bucket=bucket, Key=key
        )
        print("[S3 GetObject] Response: " + str(response))
        ships = json.loads(response["Body"].read().decode("utf-8"))
        timestamp_as_str = remove_prefix_if_exists(remove_suffix_if_exists(key, ".json"), "/")
        timestamp = datetime.strptime(timestamp_as_str, "%Y-%m-%d_%H:%M:%S")
        print(f"timestamp={timestamp} ships={str(ships)}")
        reshaped_ships = reshape(timestamp, ships)
        print(f"reshaped_ships={str(reshaped_ships)}")
        names = [
            (rs["name"], f"{rs['name']} ({rs['class']} - {rs['rarity']}) | {rs['vwap']} | {rs['totalSupply']}")
            for rs in reshaped_ships
        ]
        print(f"names={str(names)}")
        metrics = convert_to_metrics(reshaped_ships, fields)
        print(f"metrics={str(metrics)}")
        metric_names = set()
        for metric in metrics:
            metric_names.add(metric.name)
            emit_metric(metric)
        print(f"names={str(metric_names)}")
    except Exception as e:
        print("Error getting object {} from bucket {}".format(key, bucket))
        print(e)
        raise e
