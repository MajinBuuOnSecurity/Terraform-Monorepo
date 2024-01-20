module "vpc_peering_cross_account" {
  source = "cloudposse/vpc-peering-multi-account/aws"

  version = "0.19.1"
  namespace        = "eg"
  stage            = "dev"
  name             = "cluster"

  # Spoke account
  requester_aws_assume_role_arn             = "arn:aws:iam::071750480872:role/admin"
  requester_region                          = "us-east-2"
  requester_vpc_id                          = "vpc-0d3bd784d7689cf8b"
  requester_allow_remote_vpc_dns_resolution = true

  # Central account
  accepter_aws_assume_role_arn             = "arn:aws:iam::085885682061:role/admin"
  accepter_region                          = "us-east-2"
  accepter_vpc_id                          = "vpc-09ea73c9232b48d19"
  accepter_allow_remote_vpc_dns_resolution = true
}
