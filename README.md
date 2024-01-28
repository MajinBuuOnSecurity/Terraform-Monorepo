## Motivation

I wrote this code in a quick and dirty way, just to send it to a few companies that were trying to decide between the age-old `AWS Control Tower` v.s. `Landing Zone` v.s. [AWS Deployment Framework](https://github.com/awslabs/aws-deployment-framework/blob/bcc100e215912fa3dbc2f64e3a9bb161d92f822f/src/lambda_codebase/account_processing/create_account.py#L24) vs. `Terraform` vs. `Other` debate.

You should be able to understand this code within a day or two, and not have account creation be much more complicated than say, S3 bucket creation.

If you look at e.g. [AWS Control Tower Account Factory for Terraform](https://docs.aws.amazon.com/controltower/latest/userguide/aft-architecture.html) I am sure you will not be able to understand it all within a day or two, nor customize it easily to your heart's content.


### Automation

#### create_aws_account

There are [more details below](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo#create-account), but at a high-level:
1. Creates an account
1. Writes Terraform file under [`aws-organizations/accounts/`](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/tree/main/aws-organizations/accounts)
1. Outputs the `terraform import` command needed to [import](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/organizations_account#import) the generated Terraform file.

```
python -m create_aws_account --help
usage: create_aws_account [-h] --account_type ACCOUNT_TYPE --data_classification
                          DATA_CLASSIFICATION --project PROJECT --description DESCRIPTION
                          [--ou DESIRED_OU]

Creates an AWS account, writes Terraform and gives import command

options:
  -h, --help            show this help message and exit
  --account_type ACCOUNT_TYPE
                        Specify the Account Type (Production/Development/Sandbox)
  --data_classification DATA_CLASSIFICATION
                        Specify the Data Classification (Public/Internal/Confidential)
  --project PROJECT     Specify the Project
  --description DESCRIPTION
                        Give a one-liner about the account.
  --ou DESIRED_OU       Give a valid OU (parent_id) for the account.
```


#### generate_subaccount_tf

This creates 2 folders with generated Terraform in them that each call a respective module.

One is an SCP baseline, which will be applied in the context of your management account.
The other is a configuration baseline, which will be applied in the context of the subaccount.

See [`subaccounts/smoky-production`](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/tree/main/subaccounts/smoky-production) as an example.

```
python -m generate_subaccount_tf --help 
usage: generate_subaccount_tf [-h] [--only-scp-baseline] [--only-configuration-baseline]
                              --account-name ACCOUNT_NAME

Creates baseline Terraform using 2 different modules

options:
  -h, --help            show this help message and exit
  --only-scp-baseline   Only generate SCP baseline
  --only-configuration-baseline
                        Only generate configuration baseline
  --account-name ACCOUNT_NAME
                        Give a valid account name.
```

### Detailed Explaination

#### Create Account

This does the following:

1. Creates the AWS account with a name of `{args.project}-{args.account_type}` (will append `-2` if there is already an account with that name, `-5` if there are 4, etc.) The name of the 
2. Add tags of `"account_type"`, `"data_classification"`, `"project"`, `"description"` 
3. In all regions enables [EBS encryption by default](https://aws.amazon.com/blogs/aws/new-opt-in-to-default-encryption-for-new-ebs-volumes/) and deletes all [default VPCs](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html)
4. Edits the `admin` role trust policy to include the [`sts:SetSourceIdentity`](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html#id_credentials_temp_control-access_monitor-know) permission
5. Adds the managed `IAMFullAccess`, `ReadOnlyAccess`, `SecurityAudit`, `ViewOnlyAccess` policies, and a custom `EnableS3AccountPublicAccessBlock` policy, to `admin` role
6. Remove `AdministratorAccess` (`* on *`) from `admin` role
7. Moves new account to the given OU, if one was given.
8. Writes Terraform / displays `import` instructions

All this code is straightforwardly read from [\_\_main\_\_.py](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/automation/create_aws_account/__main__.py) which is only 100 lines of code.

Note: We need to change `ADMIN_NAME` in [constants.py](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/automation/create_aws_account/constants.py#L1) if you do not want `admin` to be the [name of the role made upon account creation](https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateAccount.html#API_CreateAccount_RequestParameters). (This defaults to `OrganizationAccountAccessRole`, a mouthful, if left unspecified.)

#### Generate Account Terraform

##### SCP Baseline

The `scps` baseline module will turn on a bunch of account-specific SCPs by default (the [variables.tf of the module are a bunch of bool values](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/modules/subaccount_baselines/scps/variables.tf))

Any SCP inheritance can be leveraged separately, by specifying a `parent_id` argument to the `aws_account` module ([example](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/77258df72ad91cb92f0ddafc54eff1685dcef0fc/aws-organizations/accounts/smoky_production.tf#L11)).

##### Configuration Baseline

The `configuration` baseline module will just setup IAM roles and turn on [`aws_s3_account_public_access_block`](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/modules/subaccount_baselines/configuration/s3/main.tf)

The only `import` necessary, is that of the `admin` IAM role. As it is automatically made upon account creation and we have to use it to [get into the account in the first place](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/77258df72ad91cb92f0ddafc54eff1685dcef0fc/subaccounts/smoky-production/configuration_baseline/versions.tf#L18).

Note: This assumes you setup GuardDuty and CloudTrail at the org-level, such that you do not need to re-do it for each individual account.

(I could have made it so you also need to import the e.g. 4 policy attachments of `IAMFullAccess`/`ReadOnlyAccess`/`SecurityAudit`/`ViewOnlyAccess`/`EnableS3AccountPublicAccessBlock` mentioned above, but since it is the `admin` role this felt unnecessary.)

### FAQ

#### Why do you do so much in Python and not Terraform?

Two reasons: first is the resources that are created automatically due to AWS. 
The other reason (for the case of EBS encryption region-wide) is because doing something in all regions is painful in Terraform.

Assuming you run this automation before handing an account to a customer, the SCP blocking e.g. `"ec2:DisableEbsEncryptionByDefault"` will be applied prior to a customer ever getting access to the account.

The only case where I was ambivalent as to what to do is: `s3:PutAccountPublicAccessBlock`.
We could
1. Do it upon account creation, and never Terraform it.
1. Do it upon account creation, and Terraform import it.
1. Give `admin` permission to turn it on upon account creation, Terraform the setting via `aws_s3_account_public_access_block`.

I chose option 3, as it seemed the least bad.
As with EBS encryption, an SCP blocking `"s3:PutAccountPublicAccessBlock"` will be applied prior to a customer getting access.


## Future Improvments

I wrote this code in a sloppy way just to demonstrate the idea, not use it in production. (Though I have written very similar code in a production setting, and this approach worked well.)

- Change the email list value to be configurable [rather than hard-coded](https://github.com/search?q=repo%3AMajinBuuOnSecurity%2FTerraform-Monorepo%20majinbuuonsec&type=code)
- Add tests
- Add more SCPs to `scp_baseline` (https://github.com/ScaleSec/terraform_aws_scp/tree/main/security_controls_scp/modules can be mined for SCPs.)
- Terraform a `baseline_ou` that can be used in addition to the `scp_baseline` module, in the case that we run into the [`Maximum attached per account`](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html) (5) limit.
- Add better IAM policies for `admin` and `operator`, such as service-specific IAM policies that take advantage of condition keys.
- Handling the case wherein you enable a new region at the org-level that all subaccounts can use (We would want to e.g. delete the default VPC, enable EBS encryption, in newly enabled regions.)

This lays the ground work for automatically setting up:
- Networking
- AWS Config
- SSM
- Permissions for e.g. your security team, Terraform CI/CD pipeline etc.

and many other things, upon account creation.
