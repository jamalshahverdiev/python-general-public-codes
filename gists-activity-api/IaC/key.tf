resource "aws_key_pair" "sshkey" {
  key_name   = "sshkey"
  public_key = file(var.public_key_path)
}
