import base64
import json
import logging

import boto3
from botocore.exceptions import ClientError

_LOGGER = logging.getLogger(__name__)

DEFAULT_REGION_NAME = "eu-west-1"


def get_secret_parser(secret_name, region_name=DEFAULT_REGION_NAME):
    try:
        secret = get_secret(secret_name, region_name)
    except botocore.exceptions.NoCredentialsError:
        _LOGGER.error("No credentials")
        return {}
    if secret is None:
        return {}
    return json.loads(secret)


def get_secret(secret_name, region_name=DEFAULT_REGION_NAME):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        return base64.b64decode(get_secret_value_response["SecretBinary"])
