data "template_file" "docker-init" {
  template = file("scripts/container-init.sh")
  vars = {
    API_TOKEN          = var.PIPEDIVE_API_TOKEN
    MY_PUBLIC_IP       = local.ifconfig_co_json.ip
  }
}

data "template_cloudinit_config" "cloudinit-docker" {
  gzip          = false
  base64_encode = false

  part {
    content_type = "text/x-shellscript"
    content      = data.template_file.docker-init.rendered
  }
}

resource "null_resource" "wait_for_cloudinit" {
  provisioner "local-exec" {
    command = <<-EOF
    #!/bin/bash
    state=1
    while [[ "$state" != 0 ]] ; do
      sleep 30
      echo "INFO: Still waiting for WEB start"
      curl -s -XGET http://${aws_instance.ec2instance.public_ip}:8080
      state=$(echo $?)
    done
    EOF
  }
}

