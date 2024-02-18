from argparse import ArgumentParser
from src.settings import Settings
from src.functions import (
    docker_login,
    docker_cli_login,
    check_docker_environment,
    process_images_from_file,
)

# Path to all manifests: ~/.docker/manifests
# rm -rf ~/.docker/manifests/10.100.100.100-8082_external_velero_velero-v1.2.0
# export DOCKER_CLI_EXPERIMENTAL=enabled
# DOC: https://docs.docker.com/engine/reference/commandline/manifest/


def main():
    parser = ArgumentParser("Process docker images")
    parser.add_argument(
        "-f",
        "--file",
        help="filename to be parsed",
        default=Settings.imagelist_file_path,
    )
    parser.add_argument(
        "-v", "--verbosity", help="verbosity level", action="count", default=0
    )

    docker_login(
        Settings.client,
        Settings.docker_user,
        Settings.docker_password,
        Settings.remote_repository_url,
    )
    check_docker_environment()
    docker_cli_login(
        Settings.docker_user,
        Settings.docker_password,
        Settings.remote_repository_url,
    )

    args = parser.parse_args()

    process_images_from_file(
        args.file, Settings.client, Settings.remote_repository, Settings.platforms
    )


if __name__ == "__main__":
    main()
