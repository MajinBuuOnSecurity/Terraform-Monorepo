import os

from .constants import (
    EMAIL_LIST_DOMAIN,
    EMAIL_LIST_PREFIX,
)


ACCOUNT_TEMPLATE = '''module "{tf_module_name}" {{
  source = "../../modules/resource_wrappers/aws_account"

  name = "{name}"
  email = "{email}"

  account_type = "{account_type}"
  data_classification = "{data_classification}"
  project = "{project}"
  description = "{description}"
{parent_id}}}
'''


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


def write_terraform(account_name_to_make, tags, desired_ou):
	tf_module_name = account_name_to_make.replace('-', '_')
	content_to_write = ACCOUNT_TEMPLATE.format(
		tf_module_name=tf_module_name,
		name=account_name_to_make,
		email=f"{EMAIL_LIST_PREFIX}+{account_name_to_make}@{EMAIL_LIST_DOMAIN}",
		account_type=tags['account_type'],
		data_classification=tags['data_classification'],
		project=tags['project'],
		description=tags['description'],
		# Optionally, add a line of parent_id, if needed
		parent_id=f'  parent_id = "{desired_ou}"\n' if desired_ou else ''
	)

	root_dir = get_repo_root_directory()
	assert root_dir.endswith("Terraform-Monorepo")

	new_account_tf_file = os.path.join(
		root_dir,
		'aws-organizations',
		'accounts',
		f'{tf_module_name}.tf'
	)
	print(f"new_account_tf_file is {new_account_tf_file}")
	with open(new_account_tf_file, 'w') as file:
	    file.write(content_to_write)


def display_import_instructions(account_name_to_make, account_id):
	tf_module_name = account_name_to_make.replace('-', '_')
	instructions = f"terraform import module.{tf_module_name}.aws_organizations_account.account {account_id}"
	print(f"Run `{instructions}`")
