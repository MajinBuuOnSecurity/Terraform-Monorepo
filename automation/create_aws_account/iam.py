import json

from .constants import (
    ADMIN_ROLE_NAME,
    MANAGEMENT_ACCOUNT_ID,
)

import boto3


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
    except Exception as e:
        print("Error: {}".format(str(e)))

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
    except Exception as e:
        print("Error: {}".format(str(e)))
