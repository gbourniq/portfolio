#!/usr/bin/env python
import subprocess
import sys
import tarfile
from argparse import ArgumentParser
from os import environ
from pathlib import Path
from shutil import rmtree

from dotenv import load_dotenv

# directories
DEPLOY_DIR = Path(__file__).resolve().parent
TARGET_DIR = DEPLOY_DIR / "bin/"
INCLUDE_ITEMS = [  # files / directories in root of docker_deployment dir to include
    "docker-compose.yml",
    ".env",
    "util_scripts",
]

# Files to be ignored
IGNORE_FILES = ["Dockerfile", Path(__file__).name]
GIT_IGNORE = [
    str((DEPLOY_DIR / str(relative_path, sys.stdout.encoding)).absolute())
    for relative_path in (
        subprocess.check_output(
            ["git", "ls-files", "--others", "--directory"]
        ).splitlines()
    )
]


def exclude(filename: str):
    file_path = Path(filename)
    if any([filename in GIT_IGNORE, file_path.name in IGNORE_FILES]):
        return True


def download_docker_images(
    docker_images_path: Path, clean: bool = False
) -> None:
    """
    Downloads and tars docker images into the specified path.
    """

    environment = environ.copy()
    docker_images_path.mkdir(exist_ok=True)
    subprocess.check_call(
        ["docker-compose", "up", "-d"], env=environment, cwd=DEPLOY_DIR
    )

    # Format 'docker-compose images' output, then save docker images
    subprocess.check_call(
        "docker-compose images| awk 'NR > 2' | tr -s ' ' ':' | cut -d ':' -f 2,3,4 | "
        "sed 's/\:/ -o /2' | xargs -I {} echo {}.tar.gz | xargs -L1 docker save",
        shell=True,
        cwd=docker_images_path,
    )
    params = ["--rmi", "all", "-v"] if clean else []
    subprocess.check_call(["docker-compose", "down"] + params, cwd=DEPLOY_DIR)


def build(args):
    """
    Builds a tarball for docker deployment containing an myapp
    directory with all the required config files and docker-compose
    yamls.

    .env is filled in with standard deployment variables and optionally
    with dummy passwords.

    The installation instructions are put in a directory alongside the
    myapp directory.

    The docker images can aso be optionally included.
    """

    print(
        f"Executing build function...\n\n"
        f"DEPLOY_DIR is {DEPLOY_DIR}\n"
        f"TARGET_DIR will be {TARGET_DIR}\n"
        f"Filename will be {args.name}.tar.gz\n"
    )

    env_file_path = Path(".env")
    assert env_file_path.exists()
    load_dotenv(env_file_path)

    Path(TARGET_DIR).mkdir(exist_ok=True)

    with tarfile.open(f"{TARGET_DIR}/{args.name}.tar.gz", "w:gz") as tar:

        for _file in INCLUDE_ITEMS:
            tar.add(DEPLOY_DIR / _file, arcname=f"myapp/{_file}")

        if args.docker_images:
            docker_images_path = Path("docker_images")
            download_docker_images(docker_images_path, args.clean)
            tar.add(
                docker_images_path, arcname="myapp/docker_images"
            )  # add docker images
            rmtree(docker_images_path)

    print("Completed build execution!!!")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--name",
        default="moltres_docker_deploy",
        help="Name of output file. Do not include extension!",
    )
    parser.add_argument(
        "--docker_images",
        "-di",
        action="store_true",
        help="Flag for including docker images in deploy tarball",
    )
    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        help="Flag for removing pulled images for this project.\nWARNING: This will "
        "remove images and volumes that are specified in docker-compose .yml files.",
    )
    args = parser.parse_args()
    build(args)
