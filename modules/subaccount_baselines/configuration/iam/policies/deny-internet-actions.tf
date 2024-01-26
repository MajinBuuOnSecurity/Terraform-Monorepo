# data "aws_iam_policy_document" "deny_internet_actions" {
#   statement {
#     sid = "DenyInternetActions"

#     actions = [
#       "ec2:AllocateAddress",
#       "ec2:AssociateAddress",
#       "ec2:AttachInternetGateway",
#       "ec2:CreateInternetGateway",
#       "ec2:CreatePublicIpv4Pool",
#       "ec2:ProvisionPublicIpv4PoolCidr",
#       "elasticloadbalancing:CreateLoadBalancer",
#       "eks:CreateCluster",
#     ]

#     effect = "Deny"

#     resources = [
#       "*"
#     ]
#   }
# }

# resource "aws_iam_policy" "deny_internet_actions" {
#   name   = "DenyInternetActions"
#   policy = data.aws_iam_policy_document.deny_internet_actions.json
# }
