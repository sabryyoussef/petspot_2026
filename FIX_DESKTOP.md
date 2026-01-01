# Fix Ubuntu Desktop - No Apps Showing

## Problem
Desktop environment is running but no apps/desktop icons are visible.

## Quick Fixes

### Option 1: Restart GNOME Shell (Easiest)
Press: `Alt + F2`, then type: `r` and press Enter
This restarts GNOME Shell without logging out.

### Option 2: Restart Desktop Session
1. Press: `Alt + F2`
2. Type: `gnome-session-quit --logout --force`
3. Press Enter
4. Log back in

### Option 3: Restart Display Manager (From Terminal)
```bash
sudo systemctl restart lightdm
```

### Option 4: Check if GNOME Shell Extension Issue
```bash
# Check GNOME Shell version
gnome-shell --version

# Restart GNOME Shell
killall -SIGQUIT gnome-shell
```

### Option 5: Reset GNOME Settings (Last Resort)
```bash
# Backup first
cp -r ~/.config/gnome-shell ~/.config/gnome-shell.backup

# Reset GNOME Shell
dconf reset -f /org/gnome/shell/
```

## Check Current Status

```bash
# Check if GNOME Shell is running
ps aux | grep gnome-shell

# Check display manager
systemctl status lightdm

# Check for errors
journalctl -u lightdm --since "1 hour ago" | grep -i error
```

## Common Causes

1. **GNOME Shell Extension Crash** - Disable extensions
2. **Display Driver Issue** - Check graphics drivers
3. **Memory Issue** - Check available RAM
4. **Corrupted Session** - Restart session

## If Nothing Works

Try switching to a different desktop environment or use the terminal:

```bash
# Install alternative desktop (if needed)
sudo apt install ubuntu-desktop-minimal

# Or use terminal only
# Press Ctrl+Alt+F1 to switch to terminal
```

