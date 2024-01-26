variable "regions" {
  description = "A list of regions to be used in the account"
  type        = list(string)
}

variable "services" {
  description = "A list of IAM service prefixes to be used in the account"
  type        = list(string)
}
