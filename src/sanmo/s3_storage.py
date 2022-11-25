from datetime import datetime
import json
from typing import Dict, List, Optional

import boto3
from botocore.config import Config

config = Config(region_name='us-east-1')

s3 = boto3.client('s3', config=config)

def store(store_dir: str, ships_price_info: List[Dict[str, Optional[str]]]) -> None:
    bucket = "star-atlas"
    now = datetime.now()
    key = store_dir + "/" + now.strftime("%Y-%m-%d_%H:%M:%S.json")
    content = json.dumps(ships_price_info)
    result = s3.put_object(Body=content, Bucket=bucket, Key=key)

    print("result: " + str(result))

    res = result.get('ResponseMetadata')

    if res.get('HTTPStatusCode') == 200:
        print('File Uploaded Successfully')
    else:
        print('File Not Uploaded')
