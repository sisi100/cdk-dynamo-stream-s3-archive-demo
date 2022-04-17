import os
import time

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]
TTL = 30  # 有効時間30秒

dynamo_table = boto3.resource("dynamodb").Table(TABLE_NAME)


def handler(event, context):
    print(event)
    unix_time_sec = int(time.time())
    dynamo_table.put_item(
        Item={
            "pk": "demo_app",
            "sk": str(unix_time_sec),
            "ttl": unix_time_sec + TTL,
        },
    )
