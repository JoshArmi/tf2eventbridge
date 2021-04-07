from time import time
import logging
import os

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_event_store():
    EVENT_STORE_TABLE_NAME = os.environ["EVENT_STORE_TABLE_NAME"]
    return boto3.resource("dynamodb").Table(EVENT_STORE_TABLE_NAME)


def get_time_series():
    return (
        boto3.client("timestream-write"),
        os.environ["TSDB_DB_NAME"],
        os.environ["TSDB_TABLE_NAME"].split("|")[1],
    )


def persist_event(event_store, event):
    event["PKEY"] = f'{event["source"]}#{event["detail"]["Name"]}'
    event["Timestamp"] = int(time())
    logger.info(f"Persisting event to Dynamo {event}")
    response = event_store.get_item(Key={"PKEY": event["PKEY"]})
    if "Item" not in response:
        event_store.put_item(Item=event)
    return event


def handle(event, _):
    logger.info(event)
    event_store = get_event_store()
    (client, db_name, table_name) = get_time_series()

    timestamp = persist_event(event_store, event)["Timestamp"]

    if event["source"] == "josharmi.accountcreated":
        logger.info("Writing AccountLeadTime to Timestream")
        account_name = event["detail"]["Name"]
        response = event_store.get_item(
            Key={"PKEY": f"josharmi.accountrequested#{account_name}"}
        )

        client.write_records(
            DatabaseName=db_name,
            Records=[
                {
                    "Dimensions": [
                        {"Name": "AccountName", "Value": account_name},
                        {"Name": "Type", "Value": "AccountLeadTime"},
                    ],
                    "MeasureName": "elasped_time",
                    "MeasureValue": str(timestamp - response["Item"]["Timestamp"]),
                    "MeasureValueType": "BIGINT",
                    "Time": str(timestamp),
                    "TimeUnit": "SECONDS",
                }
            ],
            TableName=table_name,
        )


    return {}
