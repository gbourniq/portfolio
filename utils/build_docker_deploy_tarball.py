#!/usr/bin/env python
import os
import subprocess
import sys
import tarfile
from argparse import ArgumentParser
from pathlib import Path
from tarfile import TarInfo
from typing import Union

from utils.colours import blueit, bolderlineit, greenit

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TARGET_DIR = ROOT_DIR / "bin"

# Path of the artefacts actually ignored from the build command
IGNORED_ARTEFACTS = {"DIR": [], "FILE": [], "GIT": []}

WHITELIST_FILES = []

WHITELIST_DIRS = ["deployment/docker-deployment/nginx/certs"]

GIT_IGNORED = []
for relative_path in subprocess.check_output(
    ["git", "ls-files", "--others", "--directory"], cwd=str(ROOT_DIR)
).splitlines():
    abs_path = (ROOT_DIR / str(relative_path, sys.stdout.encoding)).absolute()
    rel_path = os.path.relpath(abs_path, ROOT_DIR)
    if rel_path not in WHITELIST_DIRS:
        GIT_IGNORED.append(abs_path)


# EXCLUDE NON-DIRECTORY FILES
EXCLUDE_FILES = [
    Path(file)
    for file in ROOT_DIR.iterdir()
    if not file.is_dir() and file.name not in WHITELIST_FILES
]

# EXCLUDE DIRECTORY FILES
EXCLUDE_MODULES = [
    "ansible",
    "app",
    "bin",
    "build_steps",
    "deployment/docker-build",
    "utils",
    "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
]
EXCLUDE_MODULES_PATHS = [
    Path(excl_dir).absolute() for excl_dir in EXCLUDE_MODULES
]


def exclude(tarinfo) -> Union[None, TarInfo]:
    removed_prefix = "/".join(tarinfo.name.split("/")[1:])
    abs_filepath = Path(removed_prefix).absolute()

    if tarinfo.isdir() and abs_filepath in EXCLUDE_MODULES_PATHS:
        IGNORED_ARTEFACTS["DIR"].append(os.path.relpath(abs_filepath, ROOT_DIR))
        return None
    elif abs_filepath in EXCLUDE_FILES:
        IGNORED_ARTEFACTS["FILE"].append(
            os.path.relpath(abs_filepath, ROOT_DIR)
        )
        return None
    elif abs_filepath in GIT_IGNORED:
        IGNORED_ARTEFACTS["GIT"].append(os.path.relpath(abs_filepath, ROOT_DIR))
        return None
    else:
        return tarinfo


def build(args):
    print(
        f"Executing build function...\n\n"
        f"{blueit('[ROOT_DIR]')} \n{ROOT_DIR}\n\n"
        f"{blueit('[TARGET_DIR]')} \n{args.output}\n\n"
        f"{blueit('[OUTPUT FILE]')} \n{args.name}.tar.gz\n"
    )
    Path(args.output).mkdir(exist_ok=True)
    with tarfile.open(f"{args.output}/{args.name}.tar.gz", "w:gz") as tar:
        tar.add(ROOT_DIR, arcname=args.name, filter=exclude)

    print(bolderlineit("Ignored artefacts during build execution:"))
    for artefacts_type, artefacts_relpath in IGNORED_ARTEFACTS.items():
        for path in artefacts_relpath:
            print(f"{artefacts_type} - {path}")

    print(greenit("\nCompleted build execution!"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--name",
        default="docker_deploy",
        help="Name of output file. Do not include extension!",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_TARGET_DIR,
        help="Output path for files produced by this script.",
    )
    args = parser.parse_args()
    build(args)
