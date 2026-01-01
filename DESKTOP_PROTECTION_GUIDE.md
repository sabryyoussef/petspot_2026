# Desktop Protection Guide

## Problem
Desktop icons and apps disappear after login, requiring manual fixes.

## Solution
Automated monitoring and protection system.

---

## Quick Setup (Run Once)

```bash
bash /home/petspot/odoo-19/setup_desktop_protection.sh
```

This will:
1. ✅ Configure desktop icons to always be enabled
2. ✅ Create backup of desktop settings
3. ✅ Set up automatic monitoring service
4. ✅ Auto-restart GNOME Shell if it crashes

---

## What Gets Protected

### 1. Desktop Icons Extension
- Automatically enabled on boot
- Re-enabled if disabled
- Settings backed up

### 2. GNOME Shell Monitoring
- Checks every 10 minutes
- Auto-restarts if crashed
- Monitors memory usage

### 3. Settings Backup
- Backed up to: `~/.config/gnome-backup/`
- Can restore if needed

---

## Manual Commands

### Check Monitoring Status
```bash
systemctl --user status desktop-monitor.timer
```

### View Monitoring Logs
```bash
journalctl --user -u desktop-monitor.service -f
```

### Manual Fix (If Needed)
```bash
bash /home/petspot/odoo-19/prevent_desktop_issues.sh
```

### Restore Desktop Settings
```bash
dconf load /org/gnome/ < ~/.config/gnome-backup/gnome-settings-backup.txt
```

---

## Prevention Tips

### 1. Reduce Memory Usage
- Close unused applications
- Disable unnecessary GNOME extensions
- Reduce animation effects (already configured)

### 2. Avoid Extension Conflicts
- Only enable essential extensions
- Test extensions one at a time
- Keep extensions updated

### 3. Regular Maintenance
```bash
# Check desktop health
bash /home/petspot/odoo-19/monitor_desktop.sh

# Update system
sudo apt update && sudo apt upgrade
```

---

## Troubleshooting

### If Desktop Still Breaks

1. **Quick Fix:**
   ```bash
   bash /home/petspot/odoo-19/fix_desktop_icons.sh
   ```

2. **Restart GNOME Shell:**
   - Press `Alt + F2`
   - Type `r` and press Enter

3. **Full Reset:**
   ```bash
   dconf load /org/gnome/ < ~/.config/gnome-backup/gnome-settings-backup.txt
   killall -SIGQUIT gnome-shell
   ```

4. **Restart Display Manager:**
   ```bash
   sudo systemctl restart lightdm
   ```

---

## Files Created

- `prevent_desktop_issues.sh` - Initial protection setup
- `monitor_desktop.sh` - Health monitoring script
- `setup_desktop_protection.sh` - Complete setup script
- `~/.config/systemd/user/desktop-monitor.service` - Systemd service
- `~/.config/systemd/user/desktop-monitor.timer` - Timer for monitoring
- `~/.config/gnome-backup/` - Settings backup directory

---

## Status Check

After setup, verify it's working:

```bash
# Check timer is active
systemctl --user list-timers

# Check service status
systemctl --user status desktop-monitor.service

# View recent checks
journalctl --user -u desktop-monitor.service --since "1 hour ago"
```

---

## Disable Protection (If Needed)

```bash
systemctl --user stop desktop-monitor.timer
systemctl --user disable desktop-monitor.timer
```

