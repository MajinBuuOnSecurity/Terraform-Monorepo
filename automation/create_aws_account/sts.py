import os

from .constants import ADMIN_ROLE_NAME

import boto3


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

    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
    )

    credentials = response['Credentials']
    return credentials
