import time
from functools import lru_cache

from .constants import (
    ADMIN_ROLE_NAME,
    EMAIL_LIST_DOMAIN,
    EMAIL_LIST_PREFIX,
)

import boto3
import botocore.exceptions


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


def get_ou_of_account(account_id):
    org_client = boto3.client('organizations')

    for ou_id in get_all_ou_ids():
        accounts_in_ou = org_client.list_accounts_for_parent(
            ParentId=ou_id,
        )['Accounts']
        if any(
            account['Id'] == account_id
            for account in accounts_in_ou
        ):
            return ou_id

    raise ValueError(f"No OU for account_id {account_id}")


@lru_cache(maxsize=None)
def get_all_ou_ids(parent_id=None):
    """
    Response of list_roots() looks like:
        {
            "Roots": [
                {
                    "Id": "r-examplerootid111",
    """
    org_client = boto3.client('organizations')

    parent_id_is_root = False
    if not parent_id:
        org_roots = org_client.list_roots()["Roots"]
        assert len(org_roots) == 1
        parent_id = org_roots[0]["Id"]
        parent_id_is_root = True

    try:
        response = org_client.list_organizational_units_for_parent(ParentId=parent_id)
    except botocore.exceptions.ClientError:
        raise

    ou_ids = [
        ou['Id']
        for ou in response['OrganizationalUnits']
    ]

    # Recursively get OU IDs for nested OUs
    for ou_id in ou_ids:
        ou_ids.extend(get_all_ou_ids(parent_id=ou_id))

    # Add root ID to the OU IDs
    if parent_id_is_root:
        ou_ids.append(parent_id)

    return ou_ids


def move_account_to_ou(account_id, current_ou_of_account, target_ou_id):
    org_client = boto3.client('organizations')

    try:
        org_client.move_account(
            AccountId=account_id,
            DestinationParentId=target_ou_id,
            SourceParentId=current_ou_of_account,
        )
        print(f"Account {account_id} moved to OU {target_ou_id}")
    except org_client.exceptions.AccountNotFoundException:
        print(f"Account {account_id} not found.")
        raise
    except org_client.exceptions.SourceParentNotFoundException:
        print(f"Source parent OU not found.")
        raise
    except org_client.exceptions.DestinationParentNotFoundException:
        print(f"Destination parent OU not found.")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
