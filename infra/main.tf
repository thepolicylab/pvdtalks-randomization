provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_key_pair" "auth" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_key_pair" "auth" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_instance" "rishare-example-instance" {
  connection {
    # Use local SSH for connection
    user = "ubuntu"  # Default value for our AMI
    host = self.public_ip
  }

  ami                    = lookup(var.aws_amis, var.aws_region)
  instance_type          = "t2.micro"

  key_name               = aws_key_pair.auth.id
  vpc_security_group_ids = [aws_security_group.pvdtalks-public-sg.id]

  subnet_id              = aws_subnet.pvdtalks-vpc-public.id

  associate_public_ip_address = true

  # TODO (khw): For first deploy, here is where we'll actually do things
  # provisioner "remote-exec" {
  #   inline = [
  #     "sudo apt-get -y update",
  #     "sudo apt-get install -y nginx",
  #     "sudo service nginx start"
  #   ]
  # }
}
