#!/bin/bash
# Setup SSH server to accept key-based authentication
# Run this on the SERVER

set -e

echo "=========================================="
echo "SSH Server Setup for Key Authentication"
echo "=========================================="
echo ""

# Ensure .ssh directory exists with correct permissions
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Ensure authorized_keys has correct permissions
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

echo "✓ SSH directory configured"
echo ""

# Check current authorized keys
KEY_COUNT=$(wc -l < ~/.ssh/authorized_keys 2>/dev/null || echo 0)
echo "Current authorized keys: $KEY_COUNT"
echo ""

# Show server IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "Server IP: $SERVER_IP"
echo ""

echo "=========================================="
echo "Next Steps (Run on YOUR LOCAL machine):"
echo "=========================================="
echo ""
echo "1. Generate SSH key (if you don't have one):"
echo "   ssh-keygen -t ed25519"
echo "   (Press Enter to accept defaults)"
echo ""
echo "2. Copy your public key to this server:"
echo "   ssh-copy-id petspot@$SERVER_IP"
echo "   (Enter password: petspot123)"
echo ""
echo "   OR manually copy:"
echo "   cat ~/.ssh/id_ed25519.pub | ssh petspot@$SERVER_IP 'cat >> ~/.ssh/authorized_keys'"
echo ""
echo "3. Create SSH config on your LOCAL machine (~/.ssh/config):"
echo "   Host odoo-server"
echo "       HostName $SERVER_IP"
echo "       User petspot"
echo "       IdentityFile ~/.ssh/id_ed25519"
echo ""
echo "4. Test connection:"
echo "   ssh odoo-server"
echo "   (Should connect without password!)"
echo ""
echo "=========================================="
echo "Server is ready to accept SSH keys!"
echo "=========================================="
echo ""

