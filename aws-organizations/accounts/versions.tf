terraform {
  required_version = ">= 1.5"

  backend "s3" {
    bucket         = "majin-buu-tfstate"
    key            = "aws-organizations/accounts/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "majin-buu-lockid"
  }

  required_providers {
    aws = ">= 5.14.0"
  }
}
