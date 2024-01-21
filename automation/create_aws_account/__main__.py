import sys

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


def _list_aws_accounts():
    org_client = boto3.client('organizations')

    try:
        response = org_client.list_accounts()
    except ClientError:
        raise

    accounts = response['Accounts']
    account_names = {
        account['Name']
        for account in
        accounts
    }

    # todo: delete me, make a test instead
    account_names.add("hey-production")
    account_names.add("hey-production-2")

    return account_names


def _prompt_continue(prompt):
    while True:
        user_input = input(f"{prompt} (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def _get_account_name(proposed_account_name):
    existing_aws_account_names = _list_aws_accounts()

    if proposed_account_name not in existing_aws_account_names:
        return proposed_account_name

    counter = 2
    new_account_name = f"{proposed_account_name}-{counter}"
    while new_account_name in existing_aws_account_names:
        counter += 1
        new_account_name = f"{proposed_account_name}-{counter}"

    return new_account_name


def main(command_line_args=sys.argv[1:]):
    args = parse_args(command_line_args)

    _print_logo()

    proposed_account_name = f"{args.project}-{args.account_type}"
    account_name_to_make = _get_account_name(proposed_account_name)
    if proposed_account_name != account_name_to_make:
        if not _prompt_continue(f"{proposed_account_name} already exists, create {account_name_to_make} instead?"):
            print("Exiting.")
            return 0

    print(f"Okie dokie, making the account {proposed_account_name}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
