import argparse

from .constants import (
    VALID_ACCOUNT_TYPES,
    VALID_DATA_CLASSIFICATIONS,
)


def _validate_value(value, valid_types):
    if value.lower() not in valid_types:
        raise argparse.ArgumentTypeError(
            f"Invalid Account Type. Allowed values are: {', '.join(valid_types)}",
        )
    return value.lower()


def _validate_account_type(value):
    return _validate_value(value, VALID_ACCOUNT_TYPES)


def _validate_data_classification(value):
    valid_types = ("public", "internal", "confidential")
    return _validate_value(value, VALID_DATA_CLASSIFICATIONS)


def _validate_max_length(value):
    if len(value) < 256:
        return value
    raise argparse.ArgumentTypeError(f"Length of '{value}' is too long. Maximum length is 255 characters.")


def parse_args(args):
    if not args:
        args.append('--help')

    parser = argparse.ArgumentParser(
        description="Creates an AWS account, writes Terraform and gives import command",
        prog='create_aws_account',
    )

    parser.add_argument(
        "--account_type",
        help="Specify the Account Type (Production/Development/Sandbox)",
        required=True,
        type=_validate_account_type,
    )
    parser.add_argument(
        "--data_classification",
        help="Specify the Data Classification (Public/Internal/Confidential)",
        required=True,
        type=_validate_data_classification,
    )
    parser.add_argument(
        "--project",
        help="Specify the Project",
        required=True,
        type=_validate_max_length,
    )
    parser.add_argument(
        "--description",
        help="Give a one-liner about the account.",
        required=True,
        type=_validate_max_length,
    )

    return parser.parse_args()
