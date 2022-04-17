import aws_cdk as cdk
from aws_cdk import Stack

from database.infra import Database
from demo_app.infra import DemoApp

app = cdk.App()
dynamo_stream_demo_Stack = Stack(app, "DynamoStreamDemoStack")
database = Database(dynamo_stream_demo_Stack, "Database")
DemoApp(dynamo_stream_demo_Stack, "DemoApp", table=database.table)
app.synth()
