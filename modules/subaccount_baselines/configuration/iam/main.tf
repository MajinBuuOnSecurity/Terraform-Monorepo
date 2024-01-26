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
  # TODO: Maybe just output the .name or role and .arn of policy?
  roles      = [module.roles.admin_role.name]
  policy_arn = module.policies.allowlists_policy.arn
}
