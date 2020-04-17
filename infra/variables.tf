variable "aws_region" {
  description = "The region into which we will deploy resources"
  default     = "us-east-1"
}

variable "public_key_path" {
  description = "The location of the public key that will be used to access resources"
  default = "~/.ssh/id_terraform.pub"
}

variable "key_name" {
  description = "Desired name of key pair"
  default = "pvdtalks"
}

variable "aws_amis" {
  # Ubuntu Server 18.04 LTS (HVM), SSD Volume Type
  default = {
    us-east-1 = "ami-07ebfd5b3428b6f4d"
    us-east-2 = "ami-0fc20dd1da406780b"
  }
}

