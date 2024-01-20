terraform {
  required_version = ">= 1.5"

  backend "s3" {
    bucket         = "majin-buu-tfstate"
    key            = "spoke_account/network_testing.tfstate"
    region         = "us-east-2"
    dynamodb_table = "majin-buu-lockid"
  }

  required_providers {
    aws = ">= 5.14.0"
  }
}

provider "aws" {
  region     = "us-east-2"

  assume_role {
    role_arn    = "arn:aws:iam::071750480872:role/admin"
  }
}
