# TODO: Add e.g. `NotAction` support
locals {
  possible_scps = [
    # DenyLeaveOrg
    {
      include = var.deny_leave_organization,
      effect = "Deny"
      actions = ["organizations:LeaveOrganization"]
      resources = ["*"]
      conditions = []
    },
    # DenyChangingBaseline
    {
      include = var.deny_changing_baseline,
      effect = "Deny"
      actions = [
        "ec2:DisableEbsEncryptionByDefault",
        "s3:PutAccountPublicAccessBlock",
      ]
      resources = ["*"]
      conditions = []
    },
    # DenyEc2PublicAMI
    {
      include = var.deny_public_ami_ec2,
      effect = "Deny"
      actions = ["ec2:RunInstances"]
      resources = ["arn:aws:ec2:*::image/*"]
      conditions = [
        {
          test     = "Bool"
          variable = "ec2:Public"

          values = [
            "true",
          ]
        },
      ]
    },
  ]
  included_scps = flatten([
    for scp in local.possible_scps : [
      scp.include ? [scp] : []
    ]
  ])
}

data "aws_iam_policy_document" "account_1" {
  dynamic "statement" {
    for_each = local.included_scps
    content {
      effect = statement.value["effect"]
      actions = statement.value["actions"]
      resources = statement.value["resources"]
      dynamic "condition" {
        for_each = statement.value["conditions"]
        content {
          test = condition.value["test"]
          variable = condition.value["variable"]
          values = condition.value["values"]
        }
      }
    }
  }
}

resource "aws_organizations_policy" "account_1" {
  name = "account_1"
  # Not sure if needed
  # JSON messiness due to https://ramimac.me/terraform-minimized-scps
  content = jsonencode(jsondecode(data.aws_iam_policy_document.account_1.json))
}

resource "aws_organizations_policy_attachment" "account" {
  policy_id = aws_organizations_policy.account_1.id
  target_id = var.account_id
}
