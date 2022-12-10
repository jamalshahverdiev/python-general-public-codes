#!/bin/bash

cloneFolder='/root/gistapidir'
dockerComposeVersion='1.27.4'
apt update
apt remove -y docker docker-engine docker.io containerd runc
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common python3-pip && pip3 install flask
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update
apt-get install -y docker-ce docker-ce-cli containerd.io
export API_TOKEN=${API_TOKEN}
wget https://github.com/docker/compose/releases/download/$dockerComposeVersion/docker-compose-Linux-x86_64 -O /bin/docker-compose && chmod +x /bin/docker-compose

if [ -z "${MY_PUBLIC_IP}" -o -z "${API_TOKEN}" ]
then
      echo "MY Public IP: ${MY_PUBLIC_IP} || My API Token: ${API_TOKEN}" >> ~/variables-status.txt
else
      echo "\$MY_PUBLIC_IP and \$API_TOKEN variables are NOT empty" >> ~/variables-status.txt
fi

git clone 'https://github.com/jamalshahverdiev/gists-activity-api.git' $cloneFolder && cd $cloneFolder && docker-compose up -d
echo "${MY_PUBLIC_IP}" > $cloneFolder/templates/access_list.txt
