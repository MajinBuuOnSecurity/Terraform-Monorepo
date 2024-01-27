import argparse

from .organizations import get_aws_account_names


def _validate_account_name(value):
    if value in get_aws_account_names():
        return value
    raise argparse.ArgumentTypeError(f"'{value}' is not a valid account name.")


def parse_args(args):
    if not args:
        args.append('--help')

    parser = argparse.ArgumentParser(
        description="Creates baseline Terraform using 2 different modules",
        prog='generate_subaccount_tf',
    )

    parser.add_argument(
        "--only-scp-baseline",
        help="Only generate SCP baseline",
        default=False,
        action='store_true',
    )
    parser.add_argument(
        "--only-configuration-baseline",
        help="Only generate configuration baseline",
        default=False,
        action='store_true',
    )

    parser.add_argument(
        "--account-name",
        help="Give a valid account name.",
        type=_validate_account_name,
        required=True,
    )

    # Service list
    # Region list
    # Tons of bools

    return parser.parse_args()
