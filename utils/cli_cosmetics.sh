#!/bin/bash

# Define colours
export RED="\e[1;31m"
export YELLOW="\e[1;33m"
export GREEN="\033[32m"
export NC="\e[0m"

# Define functions to print coloured messages
INFO() { printf ${YELLOW}; echo "[INFO] $1"; printf ${NC}; }
MESSAGE() { printf ${NC}; echo "$1"; printf ${NC}; }
SUCCESS() { printf ${GREEN}; echo "[SUCCESS] $1"; printf ${NC}; }
WARNING() { printf ${RED}; echo "[WARNING] $1"; printf ${NC}; }

# Export functions to be used within Makefile
export -f INFO
export -f MESSAGE
export -f SUCCESS
export -f WARNING