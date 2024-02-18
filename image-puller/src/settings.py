from os import environ, path
from docker import from_env
from sys import exit

class Settings:
    docker_user = environ.get('NEXUS_DOCKER_USER')
    docker_password = environ.get('NEXUS_DOCKER_PASSWORD')
    
    if not docker_user or not docker_password:
        print("Docker username or password not found in environment variables.")
        exit(1)

    remote_repository = "10.100.100.100:8082/external"
    remote_repository_url = "10.100.100.100:8082"
    nexus_url = "http://10.100.100.100:8081"
    nexus_repo_name = "docreg"
    platforms = ["linux/amd64", "linux/arm64", "linux/arm64/v8"]
    imagelist_file_path = "imagelist.txt"

    if not path.exists(imagelist_file_path):
        print(f"The file {imagelist_file_path} does not exist.")
        exit(1)

    client = from_env()