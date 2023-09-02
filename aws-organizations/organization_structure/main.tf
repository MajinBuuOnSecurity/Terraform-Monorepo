module "organisation" {
  source  = "infrablocks/organisation/aws"
  version = "2.1.0-rc.1"

  feature_set                   = "ALL"
  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com"
  ]

  organization = {
    units = [
      {
        name = "MyProduct",
        key = "mycompany-myproduct"
        units = [
          {
            name = "Test",
            key = "mycompany-myproduct-test"
          },
          {
            name = "Development",
            key = "mycompany-myproduct-development"
          },
          {
            name = "Production",
            key = "mycompany-myproduct-production"
          }
        ]
      }
    ]
  }
}
