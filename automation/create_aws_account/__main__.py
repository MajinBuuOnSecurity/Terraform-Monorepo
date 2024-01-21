import os
import sys

from .constants import ADMIN_ROLE_NAME
from .organizations import (
    create_and_tag_account,
    get_new_account_name_if_taken,
)
from .usage import parse_args

import boto3
from botocore.exceptions import ClientError


def _print_logo():
    print("""
      ,---.  ,--.   ,--. ,---.
     /  O  \\ |  |   |  |'   .-'
    |  .-.  ||  |.'.|  |`.  `-.
    |  | |  ||   ,'.   |.-'    |
    `--' `--''--'   '--'`-----'
      ,---.                                       ,--.
     /  O  \\  ,---. ,---. ,---. ,--.,--.,--,--, ,-'  '-.
    |  .-.  || .--'| .--'| .-. ||  ||  ||      \'-.  .-'
    |  | |  |\\ `--.\\ `--.' '-' ''  ''  '|  ||  |  |  |
    `--' `--' `---' `---' `---'  `----' `--''--'  `--'
     ,-----.                        ,--.
    '  .--./,--.--. ,---.  ,--,--.,-'  '-. ,---. ,--.--.
    |  |    |  .--'| .-. :' ,-.  |'-.  .-'| .-. ||  .--'
    '  '--'\\|  |   \\   --.\\ '-'  |  |  |  ' '-' '|  |
     `-----'`--'    `----' `--`--'  `--'   `---' `--'
    """)


def _prompt_continue(prompt):
    while True:
        user_input = input(f"{prompt} (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def _get_3_parent_folders():
    # Returns e.g. Terraform-Monorepo/automation/create_aws_account
    current_file_path = os.path.abspath(__file__)

    parent_dir = os.path.dirname(current_file_path)
    # Cannot use e.g. / in role session name, so we use '.'
    return f'.'.join(parent_dir.split('/')[-3:])


def assume_role(new_account_id):
    sts_client = boto3.client('sts')
    role_arn = f'arn:aws:iam::{new_account_id}:role/{ADMIN_ROLE_NAME}'
    current_user = os.getlogin()

    role_session_name = f"{current_user}@{_get_3_parent_folders()}"
    assert len(role_session_name) <= 64

    # print(f"mah role name is: {role_session_name}")

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
    )

    credentials = response['Credentials']
    return credentials


def list_regions(credentials):
    ec2_client = boto3.client(
        'ec2',
        region_name='us-east-1',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    regions = ec2_client.describe_regions()
    region_names = [region['RegionName'] for region in regions['Regions']]
    return region_names


def main(command_line_args=sys.argv[1:]):
    args = parse_args(command_line_args)

    _print_logo()

    proposed_account_name = f"{args.project}-{args.account_type}"
    account_name_to_make = get_new_account_name_if_taken(proposed_account_name)
    if proposed_account_name != account_name_to_make:
        if not _prompt_continue(f"{proposed_account_name} already exists, create {account_name_to_make} instead?"):
            print("Exiting.")
            return 0

    print(f"Okie dokie, making the account {account_name_to_make}")
    tags = {
        "account_type": args.account_type,
        "data_classification": args.data_classification,
        "project": args.project,
        "description": args.description,
    }
    # new_account_id = create_and_tag_account(
    #     account_name_to_make,
    #     tags,
    # )
    new_account_id = "891377159200"
    print(f"Alright, done making account {new_account_id}")

    assumed_role_credentials = assume_role(new_account_id)
    available_regions = list_regions(assumed_role_credentials)
    print("Available regions after assuming the 'admin' role:")
    print(available_regions)

    return 0


if __name__ == '__main__':
    sys.exit(main())
