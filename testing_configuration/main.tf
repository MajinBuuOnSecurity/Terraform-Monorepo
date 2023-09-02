module "management_account" {
  source = "../../modules/subaccounts/configuration"

  services = ["cloudtrail", "dynamodb", "ec2", "s3"]
  regions = ["us-east-2"]
}
