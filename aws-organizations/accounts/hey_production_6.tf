module "hey_production_6" {
  source = "../../modules/resource_wrappers/aws_account"

  name = "hey-production-6"
  email = "majinbuuonsec+hey-production-6@gmail.com"

  account_type = "production"
  data_classification = "internal"
  project = "hey"
  description = "Shit"
}
