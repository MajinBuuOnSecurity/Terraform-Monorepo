data "external" "elbs_exists" {
  # This garbage is necessary, as: 
  # - `data "aws_lb"` errors out if there are no LBs
  # - `data "aws_lbs"` returns nothing by default
  # - `aws_resourcegroupstaggingapi_resources` only works on tagged resources (and can show deleted ones)
  # Alternatively, we could contribute an ELBs data resource
  # To e.g. https://github.com/cloudposse/terraform-provider-awsutils
  # And use it.
  # But I do not feel like writing Golang.
  # TODO: Pass in regions actually used, would be good.
  program = [
    "/usr/bin/python3",
    "check_if_any_elbs.py",
  ]
}

output "public_elb_arns" {
  value = jsondecode(data.external.elbs_exists.result["public_elb_arns"])
}
