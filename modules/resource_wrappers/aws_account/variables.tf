variable "name" {
  type        = string
  nullable    = false
  description = "Name of account"

  validation {
    condition     = can(regex("^([A-Z][a-z]+\\s?)+$", var.name))
    error_message = "Regex ^([A-Z][a-z]+\\s?)+$ failed for var.name."
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
    condition = contains(["Test", "Development", "Production"], var.account_type)
    error_message = "Valid values for the account_type variable are Test, Development and Production"
  }
}
