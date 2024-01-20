module "vpc" {
  source = "cloudposse/vpc/aws"

  version   = "2.1.0"
  namespace = "eg"
  stage     = "test"
  name      = "app"

  ipv4_primary_cidr_block = "10.0.0.0/16"

  assign_generated_ipv6_cidr_block = false
}

module "dynamic_subnets" {
  source = "cloudposse/dynamic-subnets/aws"
  version            = "2.4.1"
  namespace          = "eg"
  stage              = "test"
  name               = "app"
  availability_zones = ["us-east-2a","us-east-2b","us-east-2c"]
  vpc_id             = module.vpc.vpc_id
  igw_id             = [module.vpc.igw_id]
  ipv4_cidr_block    = ["10.0.0.0/16"]
}
