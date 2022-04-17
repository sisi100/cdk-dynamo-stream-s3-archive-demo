import pathlib

from aws_cdk import aws_dynamodb, aws_events, aws_events_targets, aws_lambda
from constructs import Construct


class DemoApp(Construct):
    @property
    def table(self) -> aws_dynamodb.Table:
        return self._table

    def __init__(self, scope: Construct, construct_id: str, *, table: aws_dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, construct_id)

        function = aws_lambda.Function(
            self,
            "PutItemForTableFunction",
            code=aws_lambda.Code.from_asset(str(pathlib.Path(__file__).resolve().parent.joinpath("runtime"))),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            environment={"TABLE_NAME": table.table_name},
        )
        table.grant_write_data(function)

        # 毎時間Lambdaを叩いてみる
        every_hour_rule = aws_events.Rule(
            self,
            "EveryHourCronRule",
            schedule=aws_events.Schedule.cron(minute="0", hour="*"),
        )
        every_hour_rule.add_target(aws_events_targets.LambdaFunction(function))
