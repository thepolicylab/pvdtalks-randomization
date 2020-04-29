provider "aws" {
  profile = "default"
  region  = var.aws_region
}

resource "aws_key_pair" "auth" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

resource "aws_instance" "pvdtalks-instance" {
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
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get -y update",
      "sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable",
      "sudo apt-get update",
      "sudo apt-get install -y docker-ce docker-ce-cli containerd.io",
      "sudo curl -L \"https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose\"",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "git clone https://github.com/thepolicylab/pvdtalks-randomization",
      "cd pvdtalks-randomization",
      "docker-compose up -d"
    ]
  }
}
