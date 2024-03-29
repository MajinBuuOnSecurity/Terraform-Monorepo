locals {
  supported_services = ["ec2", "eks", "elasticloadbalancing", "s3"]
  supported_regions = ["us-east-1", "us-east-2"]
}


variable "regions" {
  description = "A list of regions to be used in the account"
  type        = list(string)

  validation {
    condition = alltrue([
      # for region in var.regions : contains(local.supported_regions, region)
      for region in var.regions : contains(["us-east-1", "us-east-2"], region)
    ])
    error_message = "All strings in the list must belong to the allowed set of values: [\"us-east-1\", \"us-east-2\"]"
    # error_message = "All strings in the list must belong to the allowed set of values: ${local.supported_regions}"
  }
}

variable "services" {
  description = "A list of IAM service prefixes to be used in the account"
  type        = list(string)

  validation {
    condition = alltrue([
      for service in var.services : contains(["ec2", "eks", "elasticloadbalancing", "s3"], service)
      # for service in var.services : contains(local.supported_services, service)
    ])
    error_message = "All strings in the list must belong to the allowed set of values: \"ec2\", \"eks\", \"elasticloadbalancing\", \"s3\"]"
    # error_message = "All strings in the list must belong to the allowed set of values: ${local.supported_services}"
  }
}

variable "restrict_operator_from_internet_facing_actions" {
  description = "Enable or disable the feature"
  type        = bool
  default     = true
}
