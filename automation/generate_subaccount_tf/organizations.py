import boto3
import botocore.exceptions


def get_aws_account_names():
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


def get_aws_account_id(account_name):
    org_client = boto3.client('organizations')

    try:
        response = org_client.list_accounts()
    except botocore.exceptions.ClientError:
        raise

    accounts = response['Accounts']
    for account in accounts:
        if account_name == account['Name']:
            print(f"account is {account}")
            return account['Id']
    raise ValueError("Account dont exist")
