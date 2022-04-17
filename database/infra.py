import pathlib

from aws_cdk import (
    Duration,
    RemovalPolicy,
    aws_dynamodb,
    aws_kinesisfirehose_alpha,
    aws_kinesisfirehose_destinations_alpha,
    aws_lambda,
    aws_lambda_event_sources,
    aws_s3,
)
from constructs import Construct


class Database(Construct):
    @property
    def table(self) -> aws_dynamodb.Table:
        return self._table

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)

        # TTLを設定したDynamoDBを作成する
        table = aws_dynamodb.Table(
            self,
            "Table",
            partition_key=aws_dynamodb.Attribute(name="pk", type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(name="sk", type=aws_dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY,
            time_to_live_attribute="ttl",
            stream=aws_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
        )
        self._table = table

        # DynamoStreamを処理するLambdaを作成する
        function = aws_lambda.Function(
            self,
            "DynamoStreamFunction",
            code=aws_lambda.Code.from_asset(str(pathlib.Path(__file__).resolve().parent.joinpath("stream_runtime"))),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(60),
            handler="index.handler",
        )
        function.add_event_source(
            aws_lambda_event_sources.DynamoEventSource(
                table,
                starting_position=aws_lambda.StartingPosition.LATEST,
            ),
        )

        # アーカイブ先のバケットを作成する
        bucket = aws_s3.Bucket(
            self,
            "ItemArchiveBucket",
        )
        firehose = aws_kinesisfirehose_alpha.DeliveryStream(
            self, "Firehose", destinations=[aws_kinesisfirehose_destinations_alpha.S3Bucket(bucket)]
        )

        # Lambdaに権限とかStream名とかあげる
        firehose.grant_put_records(function)
        function.add_environment(key="FIREHOSE_NAME", value=firehose.delivery_stream_name)
