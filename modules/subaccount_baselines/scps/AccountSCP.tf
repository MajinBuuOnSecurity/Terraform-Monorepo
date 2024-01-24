locals {
  possible_scps = [
    # DenyLeaveOrg
    {
      include = true,
      # include = var.deny_leave_organization,
      effect = "Deny"
      actions = ["organizations:LeaveOrganization"]
      resources = ["*"]
      conditions = []
    },
    # DenyEc2PublicAMI
    {
      include = true,
      # include = var.deny_public_ami,
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
  content = jsonencode(jsondecode(data.aws_iam_policy_document.account_1.json))
}
