#!/bin/bash
# Fix SSH setup - Add host key and copy SSH key

echo "=========================================="
echo "Fixing SSH Setup"
echo "=========================================="
echo ""

# Add host key to known_hosts
echo "Adding server host key to known_hosts..."
ssh-keyscan -H 192.168.100.64 >> ~/.ssh/known_hosts 2>/dev/null

echo "✓ Host key added"
echo ""

# Now copy the SSH key
echo "Copying SSH key to server..."
echo "Enter password when prompted: petspot123"
echo ""

ssh-copy-id petspot@192.168.100.64

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Now create SSH config:"
echo "mkdir -p ~/.ssh"
echo "cat >> ~/.ssh/config << 'EOF'"
echo "Host odoo-server"
echo "    HostName 192.168.100.64"
echo "    User petspot"
echo "    IdentityFile ~/.ssh/id_ed25519"
echo "EOF"
echo "chmod 600 ~/.ssh/config"
echo ""
echo "Then test: ssh odoo-server"
echo ""

