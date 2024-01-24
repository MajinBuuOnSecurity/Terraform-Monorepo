variable "deny_internet_gateways_ec2" {
  type    = bool
  default = true
}

variable "deny_public_ami_ec2" {
  type    = bool
  default = true
}

# deny_imds_v1_and_max_hop
# Deny CloudFormation?
# Deny Comprehend?
# Deny SageMaker?


# EFS

variable "deny_unencrypted_actions_efs" {
  type    = bool
  default = true
}

# IAM

variable "deny_accidental_lockout_admin_iam" {
  type    = bool
  default = true
}

# should this be deny users?
variable "deny_access_keys_iam" {
  type    = bool
  default = true
}

variable "deny_root_user_iam" {
  type    = bool
  default = true
}

variable "deny_leave_organization" {
  type    = bool
  default = true
}

# Lambda

variable "deny_no_vpc_lambda" {
  type    = bool
  default = true
}

# RDS

variable "deny_unencrypted_actions_rds" {
  type    = bool
  default = true
}

# S3

variable "deny_insecure_requests_s3" {
  type    = bool
  default = true
}

variable "deny_unencrypted_uploads_s3" {
  type    = bool
  default = true
}

variable "deny_public_access_points_s3" {
  type    = bool
  default = true
}

# Allowlists

variable "regions_allowlist" {
  type    = list(string)
  default = []
}

variable "services_allowlist" {
  type    = list(string)
  default = []
}
