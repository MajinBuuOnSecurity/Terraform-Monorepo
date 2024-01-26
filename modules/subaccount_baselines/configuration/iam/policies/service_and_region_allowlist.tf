# This dumbass MVP is just gonna give service:* for every service
#
# I _would_ add a service-specific IAM policy with lots of conditional keys etc.
# In a non-MVP versions
data "aws_iam_policy_document" "allowlists" {
  statement {
    sid = "ServiceAllowlist"

    actions = [
      for item in var.services : "${item}:*"
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid = "RegionAllowlist"

    # Global Services
    # See
    # https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples_general.html#example-scp-deny-region
    # for more information.
    not_actions = [
      "a4b:*",
      "acm:*",
      "aws-marketplace-management:*",
      "aws-marketplace:*",
      "aws-portal:*",
      "budgets:*",
      "ce:*",
      "chime:*",
      "cloudfront:*",
      "config:*",
      "cur:*",
      "directconnect:*",
      "ec2:DescribeRegions",
      "ec2:DescribeTransitGateways",
      "ec2:DescribeVpnGateways",
      "fms:*",
      "globalaccelerator:*",
      "health:*",
      "iam:*",
      "importexport:*",
      "kms:*",
      "mobileanalytics:*",
      "networkmanager:*",
      "organizations:*",
      "pricing:*",
      "route53:*",
      "route53domains:*",
      "s3:GetAccountPublic*",
      "s3:ListAllMyBuckets",
      "s3:PutAccountPublic*",
      "shield:*",
      "sts:*",
      "support:*",
      "trustedadvisor:*",
      "waf-regional:*",
      "waf:*",
      "wafv2:*",
      "wellarchitected:*"
    ]

    resources = [
      "*",
    ]

    effect = "Deny"

    condition {
      test     = "StringNotEquals"
      variable = "aws:RequestedRegion"
      values = var.regions
    }
  }
}

resource "aws_iam_policy" "allowlists" {
  name   = "ServiceAndRegionAllowlists"
  policy = data.aws_iam_policy_document.allowlists.json
}
