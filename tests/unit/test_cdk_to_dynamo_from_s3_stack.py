import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_to_dynamo_from_s3.cdk_to_dynamo_from_s3_stack import CdkToDynamoFromS3Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_to_dynamo_from_s3/cdk_to_dynamo_from_s3_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkToDynamoFromS3Stack(app, "cdk-to-dynamo-from-s3")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
