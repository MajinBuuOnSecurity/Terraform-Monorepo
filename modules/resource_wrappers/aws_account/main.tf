resource "aws_organizations_account" "account" {
  name  = var.name
  email = var.email

  close_on_deletion = true
  role_name = "admin"

  # There is no AWS Organizations API for reading role_name
  lifecycle {
    ignore_changes = [role_name]
  }

  parent_id = var.parent_id

  # Required tags
  tags = {
    account_type = var.account_type
    data_classification = var.data_classification
    description = var.description
    project = var.project
  }
}
