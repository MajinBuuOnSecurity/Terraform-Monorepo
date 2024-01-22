# data "public_subnets" "subnets" {
#   regions = var.regions_in_use
# }

# data "aws_iam_policy_document" "deny_public_subnets" {
#   statement {
#     sid = "DenyBySubnetIDCond"

#     actions = [
#       "ec2:CreateFleet",
#       "ec2:ModifyFleet",
#       "ec2:RequestSpotFleet",
#       "ec2:RequestSpotInstances",
#       "ec2:RunInstances",
#       "ec2:RunScheduledInstances",
#     ]

#     effect = "Deny"

#     resources = [
#       "arn:aws:ec2:*:*:subnet/*"
#     ]

#     condition {
#       test     = "StringEquals"
#       variable = "ec2:SubnetID"

#       values = data.public_subnets.ids
#     }
#   }

#   statement {
#     sid = "DenyBySubnetArnCond"

#     # Note `ec2:RequestSpotFleet` is not here
#     # I am dangerously assuming AWS did not mess up the Service AuthZ reference again
#     actions = [
#       "ec2:CreateFleet",
#       "ec2:ModifyFleet",
#       "ec2:RequestSpotInstances",
#       "ec2:RunInstances",
#       "ec2:RunScheduledInstances",
#     ]

#     effect = "Deny"

#     resources = [
#       "arn:aws:ec2:*:*:network-interface/*",
#     ]

#     condition {
#       test     = "StringEquals"
#       variable = "ec2:Subnet"

#       values = data.public_subnets.arns
#     }
#   }
# }
