# data "aws_subnets" "public" {
#  filter {
#    name = "map-public-ip-on-launch"
#    values = [true]
#  }
# }

# data "aws_subnet" "public_subnet_map" {
#   for_each = toset(data.aws_subnets.public.ids)
#   id       = each.value
# }

# data "aws_iam_policy_document" "deny_public_subnets" {
#   statement {
#     sid = "DenyBySubnetIDCond"

#     actions = [
#       "ec2:CreateFleet",
#       "ec2:CreateNetworkInterface",
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

#       values = data.aws_subnets.public.ids
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

#       values = [
#         for subnet in data.aws_subnet.public_subnet_map : subnet.arn
#       ]
#     }
#   }
# }

# resource "aws_iam_policy" "deny_public_subnets" {
#   name   = "DenyPublicSubnets"
#   policy = data.aws_iam_policy_document.deny_public_subnets.json
# }
