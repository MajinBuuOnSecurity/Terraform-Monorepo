module "policies" {
  source = "./policies"
  services = var.services
  regions = var.regions
}

module "roles" {
  source = "./roles"
}

resource "aws_iam_policy_attachment" "admin-allowlists" {
  name       = "admin-allowlists-attachment"
  roles      = [module.roles.admin_role_name]
  policy_arn = module.policies.allowlists_policy_arn
}
