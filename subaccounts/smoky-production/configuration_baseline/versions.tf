terraform {
  required_version = ">= 1.5"

  backend "s3" {
    bucket         = "majin-buu-tfstate"
    key            = "smoky_production_configuration.tfstate"
    region         = "us-east-2"
    dynamodb_table = "majin-buu-lockid"
  }

  required_providers {
    aws = ">= 5.14.0"
  }
}

provider "aws" {
  assume_role {
    role_arn    = "arn:aws:iam::211125546669:role/admin"
  }
}

# Print whoami in the Terraform output
data "aws_caller_identity" "current" {}
