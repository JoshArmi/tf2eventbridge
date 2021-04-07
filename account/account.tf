terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_organizations_account" "account" {
  name = "delta"
  email = "a.someone@gmail.com"
}
