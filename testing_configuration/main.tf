locals {
  services = ["dynamodb", "ec2", "s3"]
  regions = ["us-east-2"]
}


module "management_account" {
  source = "../../modules/subaccounts/configuration"

  services = local.services
  regions = local.regions
}


