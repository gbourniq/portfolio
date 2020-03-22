#!/usr/bin/env python
import subprocess
import sys
import tarfile
from argparse import ArgumentParser
from pathlib import Path
from tarfile import TarInfo
from typing import Union

from utils.colours import blueit, greenit

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

WHITELIST_FILES = [
    "static_settings.py",
]

# EXCLUDE NON-DIRECTORY FILES
# Exclude all non directory files in root and docker .env
EXCLUDE_FILES = [
    str(file)
    for file in ROOT_DIR.iterdir()
    if not file.is_dir() and file.name not in WHITELIST_FILES
]
# EXCLUDE_FILES.append(ROOT_DIR / "docker_deployment/.env")

# EXCLUDE DIRECTORY FILES
EXCLUDE_MODULES = [
    "bin",
    "cluster-management",
    "deployment",
    "utils",
    "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
    "app/tests",
]


def exclude(tarinfo) -> Union[None, TarInfo]:
    chars_count = len("portfolio/")
    remove_portfolio_prefix = tarinfo.name[chars_count:]
    rel_filepath = Path(remove_portfolio_prefix)
    abs_filepath = rel_filepath.absolute()

    if tarinfo.isdir() and str(rel_filepath) in EXCLUDE_MODULES:
        print(f"DIR IGNORED:  {str(rel_filepath)}")
        return None
    elif str(abs_filepath) in EXCLUDE_FILES:
        print(f"FILE IGNORED: {str(abs_filepath)}")
        return None
    elif str(abs_filepath) in GIT_IGNORED:
        print(f"GIT IGNORED:  {str(abs_filepath)}")
        return None
    else:
        return tarinfo


def build(args):
    print(
        f"Executing build function...\n\n"
        f"{blueit('[ROOT_DIR]')} \n{ROOT_DIR}\n\n"
        f"{blueit('[TARGET_DIR]')} \n{args.output}\n\n"
        f"{blueit('[OUTPUT FILE]')} \n{args.name}.tar.gz\n\n"
    )
    Path(args.output).mkdir(exist_ok=True)
    with tarfile.open(f"{args.output}/{args.name}.tar.gz", "w:gz") as tar:
        tar.add(ROOT_DIR, arcname=args.name, filter=exclude)

    print(greenit("Completed build execution!"))


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
