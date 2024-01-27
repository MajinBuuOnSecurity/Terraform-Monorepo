## Motivation

I wrote this code in a quick and dirty way, just to send it to a few companies that were trying to decide between the age old `AWS Control Tower v.s. Landing Zone v.s. Terraform vs. Other` debate.

You should be able to understand this code within a day or two, and not have accounts be any more complicated to make than say, an S3 bucket.

If you look at e.g. [AWS Control Tower Account Factory for Terraform](https://docs.aws.amazon.com/controltower/latest/userguide/aft-architecture.html) I am sure you will not be able to understand it all within a day or two, nor customize it easily to your heart's content.


### Automation

#### create_aws_account

At a high-level:
1. [Create an account](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/automation/create_aws_account/__main__.py#L65)
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

This creates 2 folders with Terraform in them.

One is an SCP baseline, which will be applied in the context of your management account.
The other is a configuration baseline, which will be applied in the context of the subaccount.

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

### Modules
### Subaccounts/


### Detailed Explaination

#### Create Account

This does the following:

1. Creates the AWS account with a name of `{args.project}-{args.account_type}` (will append `-2` if there is already an account with that name, `-5` if there are 4, etc.) The name of the 
2. Add tags of `"account_type"`, `"data_classification"`, `"project"`, `"description"` 
3. In all regions enables [EBS encryption by default](https://aws.amazon.com/blogs/aws/new-opt-in-to-default-encryption-for-new-ebs-volumes/) and deletes all [default VPCs](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html)
4. Edits the `admin` role trust policy to include the [`sts:SetSourceIdentity`](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_monitor.html#id_credentials_temp_control-access_monitor-know) permission
5. Adds the managed `IAMFullAccess`, `ReadOnlyAccess`, `SecurityAudit`, `ViewOnlyAccess` policies, and a custom `EnableS3AccountPublicAccessBlock` policy, to `admin` role
6. Remove `AdministratorAccess` (`* on *`) from `admin` role
7. Moves new account to the given OU, if given.
8. Writes Terraform / displays `import` instructions

All this code is straightforwardly read from [__main__.py](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/automation/create_aws_account/__main__.py) which is only 100 lines of code.

Note: We need to change `ADMIN_NAME` in [constants.py](https://github.com/MajinBuuOnSecurity/Terraform-Monorepo/blob/main/automation/create_aws_account/constants.py#L1) if you do not want `admin` to be the [name of the role made upon account creation](https://docs.aws.amazon.com/organizations/latest/APIReference/API_CreateAccount.html#API_CreateAccount_RequestParameters). (This defaults to `OrganizationAccountAccessRole`, a mouthful, if left unspecified.)

#### Generate Account Terraform


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
As with EBS encrpytion, an SCP blocking ` "s3:PutAccountPublicAccessBlock"` will be applied prior to a customer getting access.



