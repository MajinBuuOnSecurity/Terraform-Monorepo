import os
import sys

from .configuration import generate_configuration_baseline
from .scps import generate_scp_baseline
from .usage import parse_args


def _print_logo():
    # Font: Slant
    # Source: https://patorjk.com
    print("""
       _____       __                                      __
      / ___/__  __/ /_  ____ _______________  __  ______  / /_
      \\__ \\/ / / / __ \\/ __ `/ ___/ ___/ __ \\/ / / / __ \\/ __/
     ___/ / /_/ / /_/ / /_/ / /__/ /__/ /_/ / /_/ / / / / /_
    /____/\\__,_/_.___/\\__,_/\\___/\\___/\\____/\\__,_/_/ /_/\\__/
       / __ )____ _________  / (_)___  ___
      / __  / __ `/ ___/ _ \\/ / / __ \\/ _ \\
     / /_/ / /_/ (__  )  __/ / / / / /  __/
    /_____/\\__,_/____/\\___/_/_/_/ /_/\\___/
      / ____/_______  ____ _/ /_____  _____
     / /   / ___/ _ \\/ __ `/ __/ __ \\/ ___/
    / /___/ /  /  __/ /_/ / /_/ /_/ / /
    \\____/_/   \\___/\\__,_/\\__/\\____/_/
    """)


def get_repo_root_directory():
    current_directory = os.getcwd()
    root_directory = None

    # Navigate upwards until reaching the root directory
    while True:
        if '.git' in os.listdir(current_directory):
            root_directory = current_directory
            break
        else:
            # Move up one level
            current_directory = os.path.dirname(current_directory)

            # Break the loop if already at the root
            if current_directory == root_directory:
                break

    return root_directory



def main(command_line_args=sys.argv[1:]):
    args = parse_args(command_line_args)

    _print_logo()

    print(f"Generating TF for the account {args.account_name}")

    get_repo_root_directory()

    root_dir = get_repo_root_directory()
    assert root_dir.endswith("Terraform-Monorepo")

    subaccount_directory = os.path.join(
        root_dir,
        'subaccounts',
        args.account_name,
    )
    os.makedirs(subaccount_directory, exist_ok=True)
    if args.only_scp_baseline:
        generate_scp_baseline(subaccount_directory)
    elif args.only_configuration_baseline:
        generate_configuration_baseline(subaccount_directory)
    else:
        generate_scp_baseline(subaccount_directory)
        generate_configuration_baseline(subaccount_directory)

    return 0


if __name__ == '__main__':
    sys.exit(main())
