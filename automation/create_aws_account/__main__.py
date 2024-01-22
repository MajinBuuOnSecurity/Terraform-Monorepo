import sys

from .ec2 import delete_all_default_vpcs
from .organizations import (
    create_and_tag_account,
    get_new_account_name_if_taken,
)
from .sts import assume_role
from .usage import parse_args


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
    delete_all_default_vpcs(assumed_role_credentials)

    return 0


if __name__ == '__main__':
    sys.exit(main())
