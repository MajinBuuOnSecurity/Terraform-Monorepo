module "smoky_production" {
  source = "../../../modules/subaccount_baselines/configuration"

  services = local.services
  regions = local.regions
}
