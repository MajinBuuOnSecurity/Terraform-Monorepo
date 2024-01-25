import os

from .organizations import get_aws_account_id


MAIN_TEMPLATE = '''module "{account_name_var}" {{
  source = "../../../modules/subaccount_baselines/scps"

  account_id = "{account_id}"
}}
'''
VERSIONS_TEMPLATE = '''terraform {{
  required_version = ">= {tf_version}"

  backend "s3" {{
    bucket         = "{state_bucket}"
    key            = "{account_name}.tfstate"
    region         = "{state_region}"
    dynamodb_table = "{state_table}"
  }}

  required_providers {{
    aws = ">= {aws_provider_version}"
  }}
}}
'''


def write_tf_file(scp_baseline_directory, filename, content):
	tf_file = os.path.join(
		scp_baseline_directory,
		filename,
	)
	with open(tf_file, 'w') as file:
	    file.write(content)


def generate_scp_baseline(subaccount_directory):
    scp_baseline_directory = os.path.join(
        subaccount_directory,
        'scp_baseline',
    )
    os.makedirs(scp_baseline_directory, exist_ok=True)

    account_name = subaccount_directory.split('/')[-1]
    account_name_var = account_name.replace('-','_')

    main_tf_content = MAIN_TEMPLATE.format(
        account_name_var=account_name_var,
        account_id=get_aws_account_id(account_name),
    )
    versions_tf_content = VERSIONS_TEMPLATE.format(
        tf_version='1.5',
        state_bucket='majin-buu-tfstate',
        account_name=account_name_var,
        state_region='us-east-2',
        state_table='majin-buu-lockid',
        aws_provider_version='5.14.0',
    )
    for (filename, content) in (
        ('versions.tf', versions_tf_content),
        ('main.tf', main_tf_content),
    ):
        write_tf_file(
            scp_baseline_directory,
            filename=filename,
            content=content,
        )

