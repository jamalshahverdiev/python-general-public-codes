variable "INSTANCE_PASSWORD" {}
variable "PIPEDIVE_API_TOKEN" {}

variable "private_key_path" {
  default = "~/.ssh/id_rsa"
}

variable "public_key_path" {
  default = "~/.ssh/id_rsa.pub"
}

variable "INSTANCE_USERNAME" {
  default = "ubuntu"
}

variable "AWS_ACCESS_KEY" {}
variable "AWS_SECRET_KEY" {}
variable "AWS_REGION" {}
variable "VPC_CIDR" {}

variable "AMIS" {
  type = map
  default = {
    us-east-1 = "ami-0be3f0371736d5394"
    us-west-2 = "ami-0c007ac192ba0744b"
    eu-west-1 = "ami-055958ae2f796344b"
  }
}
