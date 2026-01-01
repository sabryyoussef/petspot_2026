# Setup Passwordless SSH Access

## Important Note
**SSH config files cannot store passwords directly** for security reasons. However, you have two options:

---

## Option 1: SSH Keys (RECOMMENDED - Most Secure)

This is the standard and secure way to avoid typing passwords.

### On Your LOCAL Machine:

1. **Generate SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Press Enter to accept defaults
   ```

2. **Copy key to server**:
   ```bash
   ssh-copy-id petspot@192.168.100.64
   # Enter password when prompted: petspot123
   ```

3. **Create SSH config file** (`~/.ssh/config`):
   ```bash
   mkdir -p ~/.ssh
   chmod 700 ~/.ssh
   nano ~/.ssh/config
   ```
   
   Add this content:
   ```
   Host odoo-server
       HostName 192.168.100.64
       User petspot
       Port 22
       IdentityFile ~/.ssh/id_ed25519
       ServerAliveInterval 60
   ```
   
   Save and set permissions:
   ```bash
   chmod 600 ~/.ssh/config
   ```

4. **Test connection**:
   ```bash
   ssh odoo-server
   # Should connect without password!
   ```

---

## Option 2: Using sshpass (Less Secure)

If you really want to use password, you can use `sshpass` tool.

### On Your LOCAL Machine:

1. **Install sshpass**:
   ```bash
   sudo apt install sshpass
   ```

2. **Create alias** in `~/.bashrc` or `~/.zshrc`:
   ```bash
   echo 'alias ssh-odoo="sshpass -p \"petspot123\" ssh -o StrictHostKeyChecking=no petspot@192.168.100.64"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Use the alias**:
   ```bash
   ssh-odoo
   ```

### Or create a script:

Create file `~/ssh-odoo.sh`:
```bash
#!/bin/bash
sshpass -p 'petspot123' ssh -o StrictHostKeyChecking=no petspot@192.168.100.64 "$@"
```

Make it executable:
```bash
chmod +x ~/ssh-odoo.sh
```

Use it:
```bash
~/ssh-odoo.sh
```

---

## Quick Setup Script

I've created a script on the server. To use it:

1. **On your LOCAL machine**, run:
   ```bash
   # Generate key if needed
   ssh-keygen -t ed25519
   
   # Copy to server (enter password: petspot123)
   ssh-copy-id petspot@192.168.100.64
   
   # Create config
   cat >> ~/.ssh/config << 'EOF'
   Host odoo-server
       HostName 192.168.100.64
       User petspot
       IdentityFile ~/.ssh/id_ed25519
   EOF
   chmod 600 ~/.ssh/config
   
   # Test
   ssh odoo-server
   ```

---

## Server IP
**192.168.100.64** (detected from your system)

---

## Security Note

- **SSH Keys** are more secure and recommended
- **sshpass** stores password in plain text (less secure)
- Never commit passwords to version control

---

## Files Created

- `ssh_config_local_example` - Example SSH config for your local machine
- `setup_ssh_passwordless.sh` - Server-side setup script
- `ssh_with_password.sh` - Quick script using sshpass

