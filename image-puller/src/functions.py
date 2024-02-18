from subprocess import run, PIPE
from typing import List, Dict, Any
from os import path

def check_docker_environment():
    """
    Checks if the Docker environment is properly set up.

    Returns:
        bool: True if the Docker environment is set up correctly, False otherwise.
    """
    service_check = run(['systemctl', 'is-active', 'docker'], stdout=PIPE, text=True)
    if service_check.returncode != 0 or service_check.stdout.strip() != 'active':
        print("docker.service is not active.")
        return False

    if not path.exists('/var/run/docker.sock'):
        print("/var/run/docker.sock does not exist.")
        return False

    which_docker = run(['which', 'docker'], stdout=PIPE, text=True)
    if not which_docker.stdout.strip():
        print("Docker is not installed or not found in PATH.")
        return False

    print("Docker environment check passed.")
    return True

def docker_login(client: Any, username: str, password: str, registry: str) -> None:
    """
    Logs in to a Docker registry using the provided credentials.

    Args:
        client (Any): The Docker client object.
        username (str): The username for authentication.
        password (str): The password for authentication.
        registry (str): The URL of the Docker registry.

    Returns:
        None
    """
    print(f"Logging in to Docker registry {registry}...")
    client.login(username=username, password=password, registry=registry)
    
def read_file_then_close(file_path: str) -> List[str]:
    """
    Read the contents of a file and return them as a list of strings.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        List[str]: A list of strings representing the lines of the file.

    """
    with open(file_path, "r") as file:
        repository_list = file.readlines()

    return repository_list

def docker_cli_login(docker_user: str, docker_password: str, remote_repository_url: str) -> None:
    """
    Log in to the Docker registry using credentials from settings.

    Args:
        docker_user (str): The username for Docker login.
        docker_password (str): The password for Docker login.
        remote_repository_url (str): The URL of the remote Docker repository.

    Returns:
        None
    """
    login_cmd = [
        "docker", "login",
        remote_repository_url,
        "-u", docker_user,
        "-p", docker_password
    ]
    result = run(login_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Docker login failed:", result.stderr)
        exit(1)

def image_exist(remote_repository: str, repo_name: str, image_tag: str) -> bool:
    """
    Checks if the specified image exists in the remote registry using `docker manifest inspect`.

    Parameters:
    - remote_repository (str): The base URL of the remote repository.
    - repo_name (str): The name of the repository.
    - image_tag (str): The tag of the image to check.

    Returns:
    - bool: True if the image exists, False otherwise.
    """
    image = f"{remote_repository}/{repo_name}:{image_tag}"
    cmd = ["docker", "manifest", "inspect", image, "--insecure"]
    result = run(cmd, stdout=PIPE, stderr=PIPE, text=True)
    print(f"Checking if image {image} exists...")
    print(f"Docke inspect result return code: {result.stdout}")
    if result.returncode == 0:
        return True  
    else:
        return False 

def pull_tag_push_docker_images(docker_client: Any, repo_name: str, image_tag: str, remote_repository: str, platforms: List[str]) -> List[Dict[str, str]]:
    """
    Pulls, tags, and pushes Docker images to a remote repository for multiple platforms.

    Args:
        docker_client (Any): The Docker client object.
        repo_name (str): The name of the repository.
        image_tag (str): The tag of the image.
        remote_repository (str): The remote repository to push the images to.
        platforms (List[str]): The list of platforms to build the images for.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the name and architecture of the pushed images.
    """
    new_image = f"{remote_repository}/{repo_name}:{image_tag}"
    manifest_images = []

    pull = True
    if image_exist(remote_repository, repo_name, image_tag):
        pull = False
        
    if pull:    
        for image_platform in platforms:
            registry_data = docker_client.images.get_registry_data(f"{repo_name}:{image_tag}")
            
            if registry_data.has_platform(image_platform):
                split_platform = image_platform.split("/")
                platform_suffix = "-".join(split_platform[1:]) if len(split_platform) > 1 else split_platform[0]
                new_platformed_image_tag = f"{new_image}-{platform_suffix}"
                pulled_image = registry_data.pull(platform=image_platform)
                pulled_image.tag(new_platformed_image_tag)

                docker_client.images.push(new_platformed_image_tag)
                print(f"Image {new_platformed_image_tag} pushed to {remote_repository}")
                manifest_images.append({
                    "name": new_platformed_image_tag,
                    "arch": split_platform[1] if len(split_platform) > 1 else "amd64",  
                })
            else:
                print(f"Platform {image_platform} not available for {repo_name}:{image_tag}")

        return manifest_images

def create_push_manifest_list(docker_client: Any, remote_repository: str, repo_name: str, image_tag: str, manifest_images: List[Dict[str, str]]) -> None:
    """
    Creates and pushes a manifest list for a Docker image.

    Args:
        docker_client (Any): The Docker client object.
        remote_repository (str): The remote repository URL.
        repo_name (str): The name of the repository.
        image_tag (str): The tag for the new image.
        manifest_images (List[Dict[str, str]]): A list of dictionaries containing the name and architecture of the manifest images.

    Returns:
        None
    """
    if len(manifest_images) > 0:
        new_image = f"{remote_repository}/{repo_name}:{image_tag}"
        docker_manifest_create_cmd = ["docker", "manifest", "create", new_image, "--insecure"] + [
            "--amend " + x["name"] for x in manifest_images
        ]
        docker_manifest_annotate_cmds = [
            ["docker", "manifest", "annotate", new_image]
            + [x["name"], "--arch", x["arch"]]
            for x in manifest_images
        ]
        docker_manifest_push_cmd = ["docker", "manifest", "push", new_image, "--insecure"]

        for cmd in [
            docker_manifest_create_cmd,
            *docker_manifest_annotate_cmds,
            docker_manifest_push_cmd,
        ]:
            res = run(" ".join(cmd), capture_output=True, shell=True)
            if res.returncode != 0:
                print(res.args)
                print(res.stderr)

        for image in manifest_images:
            docker_client.images.remove(image["name"], force=True)

def process_images_from_file(file_path: str, client: Any, remote_repository: str, platforms: List[str]) -> None:
    """
    Process images from a file.

    Args:
        file_path (str): The path to the file containing the image repository and tag information.
        client (Any): The Docker client object.
        remote_repository (str): The remote repository to push the images to.
        platforms (List[str]): The list of platforms to build the images for.

    Returns:
        None
    """
    repository_list = read_file_then_close(file_path)
    for line in repository_list:
        if not line.strip():
            continue
        image_repo_tag = line.strip().split(':')

        if len(image_repo_tag) == 2: 
            repo_name, image_tag = image_repo_tag
            manifest_images = pull_tag_push_docker_images(client, repo_name, image_tag, remote_repository, platforms)
            # print("Manifest images prepared:", manifest_images)
            if manifest_images:
                create_push_manifest_list(client, remote_repository, repo_name, image_tag, manifest_images)
            
        else:
            print(f"Invalid image format in line: {line}")