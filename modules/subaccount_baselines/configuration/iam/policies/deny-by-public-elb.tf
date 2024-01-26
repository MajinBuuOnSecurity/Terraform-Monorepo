# data "external" "elbs_exists" {
#   # This garbage is necessary, as: 
#   # - `data "aws_lb"` errors out if there are no LBs
#   # - `data "aws_lbs"` returns nothing by default
#   # - `aws_resourcegroupstaggingapi_resources` only works on tagged resources (and can show deleted ones)
#   # Alternatively, we could contribute an ELBs data resource
#   # To e.g. https://github.com/cloudposse/terraform-provider-awsutils
#   # And use it.
#   # But I do not feel like writing Golang.
#   program = [
#     "python3",
#     "check_if_any_elbs.py",
#   ]
# }

# data "aws_iam_policy_document" "deny_public_elbs" {
#   statement {
#     sid = "DenyByElbArn"

#     actions = [
#       "elasticloadbalancing:ApplySecurityGroupsToLoadBalancer",
#       "elasticloadbalancing:AttachLoadBalancerToSubnets",
#       "elasticloadbalancing:ConfigureHealthCheck",
#       "elasticloadbalancing:CreateAppCookieStickinessPolicy",
#       "elasticloadbalancing:CreateLBCookieStickinessPolicy",
#       "elasticloadbalancing:CreateLoadBalancerListeners",
#       "elasticloadbalancing:CreateLoadBalancerPolicy",
#       "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
#     ]

#     effect = "Deny"

#     resources = [
#       data.external.elbs_exists.result.public_elbs
#     ]
#   }
# }

# resource "aws_iam_policy" "deny_public_elbs" {
#   name   = "DenyPublicELBs"
#   policy = data.aws_iam_policy_document.deny_public_elbs.json
# }
