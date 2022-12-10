# GitHub users Gists activity.
### Prerequisites:
You have the following tools installed on your computer:
   - [Terraform ](https://www.terraform.io/downloads.html "Terraform Download page")
   - [Git](https://git-scm.com/downloads "Git downloads page") 
   - [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html "AWS Cli install page")
## In order to have a working environment please follow the sequence shown below:
  - [x] Infrastructure deployment preparation
  - [x] Infrastructure deployment
  - [x] Test endpoint 
### Infrastructure deployment preparation
- Clone repository 
- Set GitHub Gist user names in the `check_users_activity.py` in the variable `usernames`. 
- Set `username` and `password` login credentials in the `src/variables.py` file in lines `5` and `6`.
- Create new `s3` bucket with the name defined in the `IaC/backend.tf` file.
- Change `public_key_path` and `private_key_path` variables to set public and private key path of EC2 instance in the `IaC/vars.tf`.
- Set `aws_access_key_id` and `aws_secret_access_key` variable values with the `aws configure`  command. Otherwise you need to set this variable values inside of the `IaC/terraform.tfvars` file. 
- Set ssh username of EC2 instance in the `IaC/vars.tf` file as the value of `INSTANCE_USERNAME` variable.
- Set `PIPEDIVE_API_TOKEN` inside of `IaC/terraform.tfvars` file which will be used as `ENVIRONMENT` variable (`docker-compose` file get this env variable inside of the `cronjob` docker container) inside `check_users_activity.py` in the EC2 instance (variable comes via `IaC/scripts/container-init.sh` script). `PIPEDIVE_API_TOKEN` token taken from PipeDrive user profile settings.
- Your public IP address automatically will be written to the `templates/access list.txt` (It is access list file to use API) file. You can add other Public IP addresses as the source after deployment of EC2 instance in `/root/gistapidir/templates/access list.txt` file. 
### Infrastructure deployment
```bash
$ cd IaC
$ terraform init 
$ terraform apply -auto-approve
```
### Test endpoint
Get instance public DNS name with the following command:
```bash
$ terraform output public_dns
```
You can test `/activity` endpoint with `username` parameter to get gist activity for the selected user:
```bash
$ curl -u 'pipedrive:pipedrive' -XGET 'http://terraform_output_public_dns:8080/activity?username=unixidzero'
```
### Code details
  Deployment prepares docker containers inside of the `EC2` instance  with `docker-compose`. 
  As the provision code `terraform` uses `scripts/container-init.sh` script. Script installs needed packages and then execute `docker-compose up` command inside of the cloned folder of all code files. In the `cronjob` container `ENTRYPOINT` will be `check_users_activity.py` script to get activities of GitHub users for all public gists (CRON execute this script each `3` hours).
  In EC2 instance `docker-compose.yml` file creates two docker containers. One of them `pipedrive` with the exposed port `8080` and another one `cronjob`.
  
**Note**: Log output of the crontab you can find inside of the `cronjob` container `/tmp/cron.log` file.

