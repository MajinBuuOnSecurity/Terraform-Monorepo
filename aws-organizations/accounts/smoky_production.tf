module "smoky_production" {
  source = "../../modules/resource_wrappers/aws_account"

  name = "smoky-production"
  email = "majinbuuonsec+smoky-production@gmail.com"

  account_type = "production"
  data_classification = "internal"
  project = "smoky"
  description = "Shit"
  parent_id = "ou-zr8n-8lg00u3s"
}
