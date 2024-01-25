ACCOUNT_TEMPLATE = '''module "{account_name}" {{
  source = "../../../modules/subaccount_baselines/scps"
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


def generate_scp_baseline(subaccount_directory):
    scp_baseline_directory = os.path.join(
        subaccount_directory,
        'scp_baseline',
    )
    os.makedirs(scp_baseline_directory, exist_ok=True)


	account_name = subaccount_directory.split('/')[-1]
	account_name_var = subaccount_directory.replace('-','_')
