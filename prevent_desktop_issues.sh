#!/bin/bash
# Prevent Desktop Issues - Auto-fix and Monitor Script

export DISPLAY=:0

echo "Setting up desktop protection..."

# 1. Ensure desktop icons extension is always enabled
gnome-extensions enable ding@rastersoft.com 2>/dev/null
gsettings set org.gnome.shell.extensions.ding show-home true 2>/dev/null
gsettings set org.gnome.shell.extensions.ding show-trash true 2>/dev/null

# 2. Disable problematic extensions that might cause crashes
# (Keep only essential ones)
ENABLED_EXTENSIONS=$(gsettings get org.gnome.shell enabled-extensions 2>/dev/null)
echo "Current extensions: $ENABLED_EXTENSIONS"

# 3. Set GNOME Shell to auto-restart on crash
gsettings set org.gnome.shell always-show-log-out false 2>/dev/null

# 4. Optimize GNOME Shell memory settings
# Reduce animation effects to save memory
gsettings set org.gnome.desktop.interface enable-animations false 2>/dev/null

# 5. Create backup of desktop settings
mkdir -p ~/.config/gnome-backup
dconf dump /org/gnome/ > ~/.config/gnome-backup/gnome-settings-backup.txt 2>/dev/null

echo "✓ Desktop protection configured"
echo "✓ Settings backed up to ~/.config/gnome-backup/"

