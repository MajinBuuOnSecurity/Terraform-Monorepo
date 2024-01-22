import json

from .constants import (
    ADMIN_ROLE_NAME,
    MANAGEMENT_ACCOUNT_ID,
)

import boto3
import botocore.exceptions


EXISTING_POLICY = f'''{{
  "Statement": [
    {{
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {{
        "AWS": "arn:aws:iam::{MANAGEMENT_ACCOUNT_ID}:root"
      }}
    }}
  ],
  "Version": "2012-10-17"
}}'''
NEW_POLICY = f'''{{
  "Statement": [
    {{
      "Action": [
        "sts:AssumeRole",
        "sts:SetSourceIdentity"
      ],
      "Effect": "Allow",
      "Principal": {{
        "AWS": "arn:aws:iam::{MANAGEMENT_ACCOUNT_ID}:root"
      }}
    }}
  ],
  "Version": "2012-10-17"
}}'''


def add_set_source_identity(credentials):
    iam_client = boto3.client(
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    try:
        response = iam_client.get_role(RoleName=ADMIN_ROLE_NAME)
    except botocore.exceptions.ClientError as e:
        print("Error: {}".format(str(e)))
        raise

    assume_role_policy_document = response['Role']['AssumeRolePolicyDocument']
    if "SetSourceIdentity" in str(assume_role_policy_document):
        print("SetSourceIdentity already in assume_role_policy_document")
        return

    curent_policy = json.dumps(
        assume_role_policy_document,
        sort_keys=True,
        indent=2,
        separators=(',', ': ')
    )
    assert curent_policy == EXISTING_POLICY

    try:
        iam_client.update_assume_role_policy(
            RoleName=ADMIN_ROLE_NAME,
            PolicyDocument=NEW_POLICY
        )
    except botocore.exceptions.ClientError as e:
        print("Error: {}".format(str(e)))
        raise


def replace_administrator_access(credentials):
    iam_client = boto3.client(
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    try:
        response = iam_client.list_attached_role_policies(RoleName=ADMIN_ROLE_NAME)
    except botocore.exceptions.ClientError as e:
        raise

    current_policy_arns = sorted(
        policy['PolicyArn']
        for policy in response['AttachedPolicies']
    )
    # Give `admin` "iam:*" and various read-only policies
    desired_policy_arns = [
        'arn:aws:iam::aws:policy/IAMFullAccess',
        'arn:aws:iam::aws:policy/ReadOnlyAccess',
        'arn:aws:iam::aws:policy/SecurityAudit',
        'arn:aws:iam::aws:policy/job-function/ViewOnlyAccess',
    ]

    if current_policy_arns == desired_policy_arns:
        print(f"{ADMIN_ROLE_NAME} already has desired policy attachments")
        return

    for policy_arn in desired_policy_arns:
        try:
            iam_client.attach_role_policy(
                RoleName=ADMIN_ROLE_NAME,
                PolicyArn=policy_arn
            )
        except botocore.exceptions.ClientError as e:
            print(f"Error attaching {policy_arn} to {ADMIN_ROLE_NAME}: {e}")

    try:
        response = iam_client.detach_role_policy(
            RoleName=ADMIN_ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess',
        )
    except botocore.exceptions.ClientError as e:
        raise

    print("All policies added. AdministratorAccess removed.")

