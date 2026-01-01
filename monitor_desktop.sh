#!/bin/bash
# Monitor Desktop Health - Run this periodically to check and fix issues

export DISPLAY=:0

# Check if GNOME Shell is running
if ! pgrep -x gnome-shell > /dev/null; then
    echo "$(date): GNOME Shell not running, restarting..."
    DISPLAY=:0 gnome-shell --replace &
    sleep 3
fi

# Check if desktop icons extension is enabled
if ! gnome-extensions list --enabled | grep -q "ding@rastersoft.com"; then
    echo "$(date): Desktop icons extension disabled, enabling..."
    gnome-extensions enable ding@rastersoft.com
    killall -SIGQUIT gnome-shell
fi

# Check memory usage
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    echo "$(date): High memory usage: ${MEM_USAGE}%"
    # Restart GNOME Shell if memory is too high
    killall -SIGQUIT gnome-shell
fi

echo "$(date): Desktop health check complete"

