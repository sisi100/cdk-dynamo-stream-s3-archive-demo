import json
import os

import boto3

FIREHOSE_NAME = os.environ["FIREHOSE_NAME"]
client = boto3.client("firehose")


def handler(event, context):
    print(event)
    for record in event["Records"]:

        if record["eventName"] == "REMOVE":

            # TTLで削除されたレコードか判断
            if record["userIdentity"]["principalId"] == "dynamodb.amazonaws.com":
                # 削除されたレコードをKinesisへ流す
                client.put_record(
                    DeliveryStreamName=FIREHOSE_NAME,
                    Record={"Data": json.dumps(record["dynamodb"]["OldImage"])},
                )
