# module "majin_buu_test_account" {
#   source = "../../modules/resource_wrappers/aws_account"

#   name = "majin buu test account"
#   email = "majinbuuonsec+majin_test_account@gmail.com"

#   account_type = "test"
#   data_classification = "public"
#   project = "hey"
#   description = "Shit"
# }

# WTF

# data "aws_resourcegroupstaggingapi_resources" "load_balancer" {
#   # resource_type_filters = ["elasticloadbalancing:loadbalancerv2"]
#   resource_type_filters = ["elasticloadbalancingv2:loadbalancer"]

#   # tag_filter {
#   #   key    = "environment"
#   #   values = ["integration"]
#   # }

#   # tag_filter {
#   #   key    = "owner"
#   #   values = ["my-company"]
#   # }
# }


# output "public_elbs" {
#   # count = length(data.aws_lb.all_elbs.id) > 0 ? 1 : 0
#   value = data.aws_resourcegroupstaggingapi_resources.load_balancer.resource_tag_mapping_list[0].resource_arn
# }




# Public EKS deny part

# data "aws_eks_clusters" "example" {}

# data "aws_eks_cluster" "example" {
#   for_each = toset(data.aws_eks_clusters.example.names)
#   name     = each.value
# }

# .vpc_config.endpoint_public_access
# == true


# output "public_eks_clusters" {
#   # count = length(data.aws_lb.all_elbs.id) > 0 ? 1 : 0
#   value = data.aws_eks_cluster.example
# }

# Public ELB Deny part

# data "external" "elbs_exists" {
#   # This garbage is necessary, as `data "aws_lb"` errors out if there are no LBs
#   # We could contribute an ELBs data resource
#   # To e.g. https://github.com/cloudposse/terraform-provider-awsutils
#   # And use it
#   program = [
#     "python3",
#     "check_if_any_elbs.py",
#   ]
# }


# output "public_elbs" {
#   # count = length(data.aws_lb.all_elbs.id) > 0 ? 1 : 0
#   value = data.external.elbs_exists.result.any_elbs
# }


# # Errors if no LBs
# data "aws_lbs" "all_elbs" {}

# output "public_elbs" {
#   # count = length(data.aws_lb.all_elbs.id) > 0 ? 1 : 0
#   value = data.aws_lbs.all_elbs
# }


# data "aws_lb" "all_elbs" {
  # name = "majin"
  # count = 1
  # "${data.external.elbs_exists.result.any_elbs ? 1 : 0}"
#   name = "majin"
# }

# output "internet_facing_elb_names" {
#   # count = length(data.aws_lb.all_elbs.id) > 0 ? 1 : 0
#   value = length(data.aws_lb.all_elbs.id) > 0 ? data.aws_lb.all_elbs.id : []
# }



# Mother fucker.
# https://github.com/hashicorp/terraform/issues/16380#issuecomment-375386696


# EC2 Deny Part

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
