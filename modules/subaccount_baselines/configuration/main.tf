module "iam" {
  source   = "./iam"
  services = var.services
  regions  = var.regions
}

module "s3" {
  source = "./s3"
}
