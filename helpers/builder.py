#!/usr/bin/env python
import subprocess
import sys
import tarfile
from argparse import ArgumentParser
from pathlib import Path

import colours

# These modules will be excluded from the build
# import bin
# import cluster-management
# import deployment
# import package
# import scripts

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TARGET_DIR = ROOT_DIR / "bin"


GIT_IGNORED = []

GIT_IGNORED = [
    str((ROOT_DIR / str(relative_path, sys.stdout.encoding)).absolute())
    for relative_path in (
        subprocess.check_output(
            ["git", "ls-files", "--others", "--directory"], cwd=str(ROOT_DIR)
        ).splitlines()
    )
]

WHITELIST_FILES = ["Makefile", "static_settings.py"]

# EXCLUDE NON-DIRECTORY FILES
# Exclude all non directory files in root and docker .env
EXCLUDE_FILES = [
    file
    for file in ROOT_DIR.iterdir()
    if not file.is_dir() and file.name not in WHITELIST_FILES
]
# EXCLUDE_FILES.append(ROOT_DIR / "docker_deployment/.env")

# EXCLUDE DIRECTORY FILES
EXCLUDE_MODULES = [
    "bin",
    "cluster-management",
    "deployment",
    "helpers" "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
]


def exclude(filename):
    filepath = Path(filename)
    if filename in GIT_IGNORED:
        return True
    if filepath.is_dir():
        return filepath.name in EXCLUDE_MODULES
    else:
        return filepath in EXCLUDE_FILES


def build(args):
    print(
        f"Executing build function...\n\n"
        f"{colours.blueit('[ROOT_DIR]')} \n{ROOT_DIR}\n\n"
        f"{colours.blueit('[TARGET_DIR]')} \n{args.output}\n\n"
        f"{colours.blueit('[OUTPUT FILE]')} \n{args.name}.tar.gz\n\n"
    )
    Path(args.output).mkdir(exist_ok=True)
    with tarfile.open(f"{args.output}/{args.name}.tar.gz", "w:gz") as tar:
        tar.add(ROOT_DIR, arcname=args.name, exclude=exclude)

    print(colours.greenit("Completed build execution!"))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--name",
        default="portfolio",
        help="Name of output file. Do not include extension!",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_TARGET_DIR,
        help="Output path for files produced by this script.",
    )
    args = parser.parse_args()
    build(args)
