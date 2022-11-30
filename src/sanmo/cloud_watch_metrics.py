import boto3
from botocore.config import Config

from sanmo.model import Metric

config = Config(region_name="us-east-1")
cw = boto3.client("cloudwatch", config=config)


def emit_metric(metric: Metric) -> None:
    print("[CW PutMetricData] Sending metric: " + str(metric))
    response = cw.put_metric_data(
        Namespace=metric.namespace,
        MetricData=[
            {
                "MetricName": metric.name,
                "Dimensions": [{"Name": d.name, "Value": d.value} for d in metric.dimensions],
                "Timestamp": metric.timestamp,
                "Value": metric.value,
                "Unit": metric.unit,
            },
        ],
    )
    print("[CW PutMetricData] Response: " + str(response))
