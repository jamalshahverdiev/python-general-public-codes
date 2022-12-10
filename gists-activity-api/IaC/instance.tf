resource "aws_instance" "ec2instance" {
  ami                    = "${lookup(var.AMIS, var.AWS_REGION)}"
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.allow-ssh.id, aws_security_group.allow-web.id]
  subnet_id              = aws_subnet.main-public-1.id
  key_name               = aws_key_pair.sshkey.key_name
  user_data 		         = data.template_cloudinit_config.cloudinit-docker.rendered
}