import os

from .organizations import get_aws_account_id


LOCALS_TEMPLATE = '''locals {
  services = ["ec2", "s3"]
  regions = ["us-east-1"]
}
'''
MAIN_TEMPLATE = '''module "{account_name_var}" {{
  source = "../../../modules/subaccount_baselines/configuration"

  services = local.services
  regions = local.regions
}}
'''
VERSIONS_TEMPLATE = '''terraform {{
  required_version = ">= {tf_version}"

  backend "s3" {{
    bucket         = "{state_bucket}"
    key            = "{account_name}_configuration.tfstate"
    region         = "{state_region}"
    dynamodb_table = "{state_table}"
  }}

  required_providers {{
    aws = ">= {aws_provider_version}"
  }}
}}

provider "aws" {{
  assume_role {{
    role_arn    = "arn:aws:iam::{account_id}:role/admin"
  }}
}}

# Print account ID in the Terraform output
data "aws_caller_identity" "current" {{}}
'''


def _write_tf_file(configuration_baseline_directory, filename, content):
	tf_file = os.path.join(
		configuration_baseline_directory,
		filename,
	)
	with open(tf_file, 'w') as file:
	    file.write(content)


def generate_configuration_baseline(subaccount_directory):
    configuration_baseline_directory = os.path.join(
        subaccount_directory,
        'configuration_baseline',
    )
    os.makedirs(configuration_baseline_directory, exist_ok=True)

    account_name = subaccount_directory.split('/')[-1]
    account_name_var = account_name.replace('-','_')

    main_tf_content = MAIN_TEMPLATE.format(
        account_name_var=account_name_var,
        account_id=get_aws_account_id(account_name),
    )
    # TODO: Programmatically get latest TF version
    # TODO: Programmatically get latest AWS provider version
    # TODO: Pass in bucket/region/table as an argument
    versions_tf_content = VERSIONS_TEMPLATE.format(
        tf_version='1.5',
        state_bucket='majin-buu-tfstate',
        account_name=account_name_var,
        state_region='us-east-2',
        state_table='majin-buu-lockid',
        aws_provider_version='5.14.0',
        account_id=get_aws_account_id(account_name),
    )
    for (filename, content) in (
        ('versions.tf', versions_tf_content),
        ('main.tf', main_tf_content),
        ('locals.tf', LOCALS_TEMPLATE),
    ):
        _write_tf_file(
            configuration_baseline_directory,
            filename=filename,
            content=content,
        )

