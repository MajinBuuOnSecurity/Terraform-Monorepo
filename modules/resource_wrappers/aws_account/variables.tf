variable "name" {
  type        = string
  nullable    = false
  description = "Name of account"

  validation {
    condition     = can(regex("^([-a-z0-9]+\\s?)+$", var.name))
    error_message = "Regex ^([-a-z0-9]+\\s?)+$ failed for var.name."
  }
}

variable "email" {
  type        = string
  nullable    = false
  description = "Email address of account"

  validation {
    condition = startswith(var.email, "majinbuuonsec+")
    error_message = "Valid values for the email variable must start with majinbuuonsec+"
  }

  validation {
    condition = endswith(var.email, "@gmail.com")
    error_message = "Valid values for the email variable must end with @gmail.com"
  }
}

variable "account_type" {
  type        = string
  nullable    = false
  description = "Type of account"

  validation {
    condition = contains(["test", "development", "production"], var.account_type)
    error_message = "Valid values for the account_type variable are test, development and production"
  }
}

variable "data_classification" {
  type        = string
  nullable    = false
  description = "Data Classification (Public/Internal/Confidential)"

  validation {
    condition = contains(["public", "internal", "confidential"], var.data_classification)
    error_message = "Valid values for the data_classification variable are public, internal and confidential"
  }
}

variable "description" {
  type        = string
  nullable    = false
  description = "Description of account"
}

variable "project" {
  type        = string
  nullable    = false
  description = "Project of account"
}
