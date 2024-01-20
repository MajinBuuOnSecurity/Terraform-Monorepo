# # Allocating three Elastic IPs for high-availability and auto-scaling in the
# # cross-zone mode.
# resource "aws_eip" "nat" {
#   count = 3

#   tags = {
#     "discriminat" : "some-comment",
#     "Name" : "egress-ip-reserved"
#   }

#   lifecycle {
#     # change to `true` if this IP address has been shared with third parties
#     prevent_destroy = false
#   }
# }

# # Deploying a new VPC in two AZs with Public and Private Subnets.
# module "aws_vpc" {
#   source  = "terraform-aws-modules/vpc/aws"
#   version = "> 3, < 6"

#   name = "discriminat-example"

#   cidr = "172.16.0.0/16"

#   enable_dns_support   = true
#   enable_dns_hostnames = true

#   azs             = ["us-east-2a", "us-east-2b"]
#   public_subnets  = ["172.16.11.0/24", "172.16.21.0/24"]
#   private_subnets = ["172.16.12.0/24", "172.16.22.0/24"]

#   map_public_ip_on_launch = false

#   manage_default_security_group  = true
#   default_security_group_ingress = []
#   default_security_group_egress  = []
# }

# # Deploying an EC2 VPC Endpoint.
# module "aws_vpc_endpoints" {
#   source  = "terraform-aws-modules/vpc/aws//modules/vpc-endpoints"
#   version = "> 3, < 6"

#   vpc_id = module.aws_vpc.vpc_id

#   endpoints = {
#     ec2 = {
#       service             = "ec2"
#       private_dns_enabled = true
#       security_group_ids  = [aws_security_group.vpce_ec2.id]
#       subnet_ids          = module.aws_vpc.private_subnets
#     }
#   }

#   tags = {
#     "Name" : "ec2"
#   }
# }

# # A Security Group that allows the entire VPC to use the EC2 VPC Endpoint.
# resource "aws_security_group" "vpce_ec2" {
#   name        = "vpce-ec2"
#   description = "ingress from entire vpc to ec2 endpoint for connectivity to it without public ips"

#   vpc_id = module.aws_vpc.vpc_id

#   ingress {
#     from_port   = 443
#     to_port     = 443
#     protocol    = "tcp"
#     cidr_blocks = [module.aws_vpc.vpc_cidr_block]

#     description = "only https standard port needed for ec2 api"
#   }

#   tags = {
#     "Name" : "vpce-ec2"
#   }
# }

# # Deploying DiscrimiNAT.
# module "discriminat" {
#   source = "ChaserSystems/discriminat-gwlb/aws"

#   public_subnets  = module.aws_vpc.public_subnets
#   private_subnets = module.aws_vpc.private_subnets

#   depends_on = [module.aws_vpc_endpoints]
# }

# # Updating route tables of Private Subnets with Gateway Load Balancer Endpoint
# # routes for Internet access.
# resource "aws_route" "discriminat" {
#   count = length(module.aws_vpc.private_subnets)

#   destination_cidr_block = "0.0.0.0/0"
#   route_table_id         = module.discriminat.target_gwlb_endpoints[count.index].route_table_id
#   vpc_endpoint_id        = module.discriminat.target_gwlb_endpoints[count.index].id
# }





# This was using cloudposse VPC for basic stuff:

module "vpc" {
  source = "cloudposse/vpc/aws"

  version   = "2.1.0"
  namespace = "eg"
  stage     = "test"
  name      = "app"

  ipv4_primary_cidr_block = "10.255.0.0/16"

  # assign_generated_ipv6_cidr_block = true
  # ipv6_egress_only_internet_gateway_enabled = true
  # internet_gateway_enabled = false
}

module "dynamic_subnets" {
  source = "cloudposse/dynamic-subnets/aws"
  version            = "2.4.1"
  namespace          = "eg"
  stage              = "test"
  name               = "app"
  availability_zones = ["us-east-2a", "us-east-2b"]
  vpc_id             = module.vpc.vpc_id
  igw_id = [module.vpc.igw_id]
  ipv4_cidr_block    = ["10.255.0.0/16"]

}
