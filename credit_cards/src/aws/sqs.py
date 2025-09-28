import json
import os

import boto3

QUEUE_URL = os.getenv("SQS_QUEUE_URL")


def send_verify_status_message(ruv: str, credit_card_id: str, user_email: str):
    sqs = boto3.client("sqs", region_name="us-east-1")

    message_body = {
        "ruv": ruv,
        "credit_card_id": credit_card_id,
        "user_email": user_email,
    }

    response = sqs.send_message(
        QueueUrl=QUEUE_URL, MessageBody=json.dumps(message_body)
    )

    return response
