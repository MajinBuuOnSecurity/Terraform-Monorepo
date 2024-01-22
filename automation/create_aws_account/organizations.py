import time

from .constants import (
    ADMIN_ROLE_NAME,
    EMAIL_LIST_DOMAIN,
    EMAIL_LIST_PREFIX,
)

import boto3


def create_and_tag_account(
    new_account_name,
    tags,
):
    org_client = boto3.client('organizations')

    response = org_client.create_account(
        Email=f"{EMAIL_LIST_PREFIX}+{new_account_name}@{EMAIL_LIST_DOMAIN}",
        AccountName=new_account_name,
        RoleName=ADMIN_ROLE_NAME,
    )["CreateAccountStatus"]

    while response["State"] == "IN_PROGRESS":
        response = org_client.describe_create_account_status(
            CreateAccountRequestId=response["Id"]
        )["CreateAccountStatus"]
        if response.get("FailureReason"):
            raise IOError(
                f"Failed to create account {new_account_name}: "
                f"{response['FailureReason']}"
            )
        time.sleep(1)

    create_account_tags(
        response["AccountId"],
        tags,
    )

    # Per https://github.com/thiezn/awsaccountmgr/blame/12dd6c43df4689e5fcac35652ffb325dcd754a51/awsaccountmgr/organization.py#L270
    time.sleep(10)

    return response["AccountId"]


def create_account_tags(
    account_id,
    tags,
):
    org_client = boto3.client('organizations')

    formatted_tags = [
        {
            "Key": key,
            "Value": value,
        }
        for key, value in tags.items()
    ]

    try:
	    response = org_client.tag_resource(
            ResourceId=account_id,
            Tags=formatted_tags,
        )
    except botocore.exceptions.ClientError:
        raise

    print(f"so response is {response}")


def _get_aws_account_names():
    org_client = boto3.client('organizations')

    try:
        response = org_client.list_accounts()
    except botocore.exceptions.ClientError:
        raise

    accounts = response['Accounts']
    existing_account_names = {
        account['Name']
        for account in
        accounts
    }

    # todo: delete me, make a test instead
    # existing_account_names.add("hey-production")
    # existing_account_names.add("hey-production-2")

    return existing_account_names


def get_new_account_name_if_taken(proposed_account_name):
    existing_aws_account_names = _get_aws_account_names()

    if proposed_account_name not in existing_aws_account_names:
        return proposed_account_name

    counter = 2
    new_account_name = f"{proposed_account_name}-{counter}"
    while new_account_name in existing_aws_account_names:
        counter += 1
        new_account_name = f"{proposed_account_name}-{counter}"

    return new_account_name
