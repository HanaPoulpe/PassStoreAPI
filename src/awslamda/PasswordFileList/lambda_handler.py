"""Password File GET lambda handler"""
import functools
import json
import os
import typing

import aws_lambda_powertools
import aws_lambda_powertools.utilities.typing as aws_typing
import aws_lambda_powertools.utilities.data_classes as aws_data_classes
import boto3

# Environment
PASSWORD_FILE_BUCKET = os.getenv("PASSWORD_FILE_BUCKET", "test_bucket")
PASSWORD_FILE_BUCKET_REGION = os.getenv("PASSWORD_FILE_BUCKET_REGION", "eu-west-3")
USER_DYNAMODB_TABLE = os.getenv("USER_DYNAMODB_TABLE", "test_table")

# Globals
logger = aws_lambda_powertools.Logger(service="PasswordFile")


# Classes
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
    logger.debug(event.body)
    if event.http_method != "GET":
        return lambda_return({
            "status_code": 405,
            "body": "Method not allow on this endpoint"
        })

    if event.body:
        msg = "Malformed request body: expected empty body"
        logger.error(msg)
        return lambda_return({
            "status_code": 400,
            "error_message": msg
        })

    # Check request identity
    identity = event.request_context.identity
    logger.info(f"Got identity: {identity!r}")
    if not identity.user:
        logger.error(f"No user passed.")
        return lambda_return({
            "status_code": 403,
            "error_message": "Access denied"
        })
    groups = get_user_groups(identity.user)

    # List files
    file_list = get_file_list(groups)

    return lambda_return({
        "status_code": 200,
        "files": [f for f in file_list]
    })


def get_file_list(groups: typing.Set[str]) -> typing.Generator[typing.Dict[str, str], None, None]:
    """
    Return a accessible file list generator
    :param groups: Group set to check the access
    :return: generator of {file_name, version_id, last_updated, owner_id, access_level}
    """
    def return_dict(f_name: str,
                    v_id: str,
                    last_updated: str,
                    o_id: str,
                    access_level: str):
        """Create file dict"""
        return {
            "file_name": f_name,
            "version_id": v_id,
            "last_updated": last_updated,
            "owner_id": o_id,
            "access_level": access_level
        }

    # Get file list
    s3_client = boto3.client("s3", region_name=PASSWORD_FILE_BUCKET_REGION)
    logger.info(f"List files from s3://{PASSWORD_FILE_BUCKET}")
    files = s3_client.list_objects_v2(
        Bucket=PASSWORD_FILE_BUCKET
    )["Contents"]

    # For each file
    for f in files:
        file_name = f["Key"]
        last_modified = f["LastModified"]
        tags = get_obj_tag(s3_client,
                           {"Bucket": PASSWORD_FILE_BUCKET, 'Key': file_name})
        version_id = tags["VersionId"]
        tags = tags["TagSet"]
        owner_id = tags["Owner"]

        # Check access
        if owner_id in groups:
            yield return_dict(file_name, version_id, last_modified, owner_id, "owner")
            continue

        if not groups.isdisjoint(tags.get("WriteGroups", "").split(",")):
            yield return_dict(file_name, version_id, last_modified, owner_id, "write")
            continue

        if not groups.isdisjoint(tags.get("ReadGroups", "").split(",")):
            yield return_dict(file_name, version_id, last_modified, owner_id, "read")
            continue


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
