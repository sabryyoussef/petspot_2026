#!/bin/bash
# Quick SSH connection script with password
# Usage: ./ssh_with_password.sh

# Install sshpass if not installed
if ! command -v sshpass &> /dev/null; then
    echo "Installing sshpass..."
    sudo apt update && sudo apt install -y sshpass
fi

# Connect to server
sshpass -p 'petspot123' ssh -o StrictHostKeyChecking=no petspot@192.168.100.64 "$@"

