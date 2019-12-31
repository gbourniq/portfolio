#!/bin/bash

set -xe #  exit as soon as any command returns a nonzero status

# Running ansible playbook to clone github repo
make ansible-clone-repo