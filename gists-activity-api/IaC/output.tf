output "public_ip" {
  value = aws_instance.ec2instance.public_ip
}

output "public_dns" {
  value = aws_instance.ec2instance.public_dns
}

output "my_ip_addr" {
  value = local.ifconfig_co_json.ip
}

