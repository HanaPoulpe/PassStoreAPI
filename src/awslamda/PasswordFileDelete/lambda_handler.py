"""Password File GET lambda handler"""
import base64
import dataclasses
import datetime
import functools
import json
import os
import typing

import aws_lambda_powertools
import aws_lambda_powertools.utilities.typing as aws_typing
import aws_lambda_powertools.utilities.data_classes as aws_data_classes
import boto3
import botocore.exceptions

# Environment
PASSWORD_FILE_BUCKET = os.getenv("PASSWORD_FILE_BUCKET", "test_bucket")
PASSWORD_FILE_BUCKET_REGION = os.getenv("PASSWORD_FILE_BUCKET_REGION", "eu-west-3")
USER_DYNAMODB_TABLE = os.getenv("USER_DYNAMODB_TABLE", "test_table")

# Globals
logger = aws_lambda_powertools.Logger(service="PasswordFile")


# Classes
@dataclasses.dataclass(frozen=True)
class EventBody:
    """Basic Event body"""
    file_name: str
    file_version: str
    last_updated_utc: datetime.datetime

    @property
    def object_dict(self) -> dict:
        """S3 Dictionary"""
        if self.file_version:
            return {
                "Bucket": PASSWORD_FILE_BUCKET,
                "Key": self.file_name,
                "VersionId": self.file_version
            }
        return {
            "Bucket": PASSWORD_FILE_BUCKET,
            "Key": self.file_name
        }


class S3Client(typing.Protocol):
    """Minimal S3Client for tagging"""
    def get_object_tagging(self, **kwargs) -> dict:
        """Retrieve object tags"""
        ...


# Functions
@logger.inject_lambda_context
@aws_data_classes.event_source(data_class=aws_data_classes.APIGatewayProxyEvent)
def lambda_handler(event: aws_data_classes.APIGatewayProxyEvent,
                   context: aws_typing.LambdaContext) -> typing.Dict[str, typing.Any]:
    """AWS Lambda event handler"""
    # Checking Event
    logger.info("Checking event...")
    logger.debug(json.dumps(event))
    if event.http_method != "DELETE":
        return lambda_return({
            "status_code": 405,
            "body": "Method GET not allow on this endpoint"
        })
    try:
        event_json = event.json_body
        event_json["last_updated_utc"] = datetime.datetime.fromisoformat(
            event_json["last_updated_utc"])
        event_body = EventBody(**event.json_body)
    except (json.JSONDecodeError, TypeError, KeyError) as err:
        logger.error(f"Malformed request body: {err!r}")
        return lambda_return({
            "status_code": 400,
            "error_message": str(err)
        })

    # Check request identity
    identity = event.request_context.identity
    logger.info(f"Got identity: {identity!r}")
    if not identity.user:
        logger.error(f"No user passed.")
        return lambda_return({
            "status_code": 403,
            "file_name": event_body.file_name,
            "error_message": "Access denied"
        })
    groups = get_user_groups(identity.user)

    # Check file access list
    access = check_allowed_file(event_body, groups)
    if access == "DENIED":
        logger.error(f"Access denied for {identity} to {event_body.file_name}.")
        return lambda_return({
            "status_code": 403,
            "file_name": event_body.file_name,
            "error_message": "Access denied"
        })

    # Checks if file exists
    if access == "NOT FOUND":
        logger.error(f"File {event_body.file_name} not found.")
        return lambda_return({
            "status_code": 404,
            "file_name": event_body.file_name,
            "error_message": "File not found"
        })

    logger.info(f"Access Granted to {identity} on {event_body.file_name}.")
    return lambda_return({
        "status_code": 200,
        **delete_file(event_body)
    })


def check_allowed_file(event_body: EventBody, user_groups: typing.Set[str]) -> str:
    """
    Check if user is allowed to read the file

    :param event_body: Event body with file name
    :param user_groups: List of group ids
    :return: "OK"|"DENIED"|"NOT FOUND"
    """
    s3_client = boto3.client("s3", region_name=PASSWORD_FILE_BUCKET_REGION)

    logger.debug(f"Reading tags for s3://{PASSWORD_FILE_BUCKET}/{event_body.file_name}")
    try:
        tags: dict = get_obj_tag(s3_client, event_body.object_dict)
    except botocore.exceptions.ClientError as err:
        logger.error(f"Got error {err} while reading tags.")
        if err.response["Error"]["Code"] == "NoSuchKey":
            return "NOT FOUND"
        if err.response["HTTPStatusCode"] == 403:  # Access denied
            return "DENIED"
        raise err

    access_groups = tags["TagSet"].get("WriteGroups", "").split(",")
    logger.debug(f"Autorized groups: {access_groups}")

    if user_groups.isdisjoint(access_groups):
        return "DENIED"

    return "OK"


def delete_file(event_body: EventBody) -> typing.Dict[str, typing.Any]:
    """
    Read files from S3, and pepare the return dict

    :param event_body: Event body
    :return: {
            "file_name": str,
            "owner_id": str,
            "last_updated": str,
            "version_id": str,
            "checksum": str,
            "content": str
            }
    """
    s3_client = boto3.client("s3", region_name=PASSWORD_FILE_BUCKET_REGION)

    # Get file
    try:
        logger.debug(f"Deleting file: s3://{PASSWORD_FILE_BUCKET}/{event_body.file_name}")
        s3_response = s3_client.delete_object(**event_body.object_dict)
    except botocore.exceptions.ClientError as err:
        logger.error(f"Error deleting file")
        raise err
    version_id = s3_response["VersionId"]
    last_updated = datetime.datetime.utcnow()

    return {
        "file_name": event_body.file_name,
        "last_updated": last_updated.isoformat(),
        "version_id": version_id,
    }


@functools.lru_cache
def get_obj_tag(s3_client: S3Client, params: dict) -> dict:
    """Cached version of s3 client get_object_tagging"""
    return s3_client.get_object_tagging(**params)


def get_user_groups(user_id: str) -> typing.Set[str]:
    """Get the list of group the user can read"""
    logger.info(f"Retrieving groups for user {user_id}")
    dynamo_client = boto3.client("dynamodb", region_name=PASSWORD_FILE_BUCKET_REGION)

    item = dynamo_client.get_item(
        TableName=USER_DYNAMODB_TABLE,
        Key={
            "object_id": {
                "S": f"uid:{user_id}"
            }
        },
        AttributesToGet=[
            "groups"
        ]
    )

    if not item["Item"]:
        return set()

    return item["Item"]["groups"].get("SS", set()).union({user_id})


def lambda_return(body: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
    """Format lambda return"""
    return {
        "statusCode": body["status_code"],
        "body": json.dumps(body)
    }

