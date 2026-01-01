#!/bin/bash
# Restart GNOME Shell and Desktop Environment

echo "Restarting GNOME Shell..."

# Method 1: Restart GNOME Shell process
killall -SIGQUIT gnome-shell 2>/dev/null
sleep 2

# Method 2: If that doesn't work, restart the session
if ! pgrep -x gnome-shell > /dev/null; then
    echo "GNOME Shell stopped, restarting..."
    DISPLAY=:0 gnome-shell --replace &
    sleep 3
fi

# Method 3: Check if it's running
if pgrep -x gnome-shell > /dev/null; then
    echo "✓ GNOME Shell is running"
else
    echo "✗ GNOME Shell failed to start"
    echo "Try: sudo systemctl restart lightdm"
fi

