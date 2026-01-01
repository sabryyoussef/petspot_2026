#!/bin/bash
# Setup passwordless SSH access TO this server
# Run this on the SERVER to prepare for key-based authentication

echo "=========================================="
echo "SSH Passwordless Setup (Server Side)"
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
echo "To enable passwordless login FROM your local machine:"
echo ""
echo "1. On your LOCAL machine, generate SSH key (if needed):"
echo "   ssh-keygen -t ed25519 -C 'your_email@example.com'"
echo "   (Press Enter to accept defaults)"
echo ""
echo "2. Copy your public key to this server:"
echo "   ssh-copy-id petspot@192.168.100.62"
echo ""
echo "   OR manually:"
echo "   cat ~/.ssh/id_ed25519.pub | ssh petspot@192.168.100.62 'cat >> ~/.ssh/authorized_keys'"
echo ""
echo "3. Create SSH config on your LOCAL machine (~/.ssh/config):"
echo "   Host odoo-server"
echo "       HostName 192.168.100.62"
echo "       User petspot"
echo "       IdentityFile ~/.ssh/id_ed25519"
echo ""
echo "4. Then connect with: ssh odoo-server"
echo ""
echo "Current authorized keys:"
wc -l ~/.ssh/authorized_keys 2>/dev/null || echo "0"
echo ""

