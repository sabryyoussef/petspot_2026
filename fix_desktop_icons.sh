#!/bin/bash
# Fix Desktop Icons and Apps Visibility

export DISPLAY=:0

echo "Fixing desktop icons and apps..."

# Enable desktop icons extension
gnome-extensions enable ding@rastersoft.com 2>/dev/null || echo "Extension already enabled"

# Show desktop icons
gsettings set org.gnome.shell.extensions.ding show-home true 2>/dev/null
gsettings set org.gnome.shell.extensions.ding show-trash true 2>/dev/null
gsettings set org.gnome.shell.extensions.ding show-volumes true 2>/dev/null

# Restart GNOME Shell to apply changes
killall -SIGQUIT gnome-shell

echo "Done! Desktop icons should appear after GNOME Shell restarts."

