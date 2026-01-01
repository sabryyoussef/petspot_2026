#!/bin/bash
# Setup Desktop Protection - Run once to configure

echo "=========================================="
echo "Setting Up Desktop Protection"
echo "=========================================="
echo ""

# Make scripts executable
chmod +x /home/petspot/odoo-19/prevent_desktop_issues.sh
chmod +x /home/petspot/odoo-19/monitor_desktop.sh

# Run initial setup
bash /home/petspot/odoo-19/prevent_desktop_issues.sh

# Create systemd user service for monitoring
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/desktop-monitor.service << 'EOF'
[Unit]
Description=Desktop Health Monitor
After=graphical-session.target

[Service]
Type=oneshot
ExecStart=/home/petspot/odoo-19/monitor_desktop.sh
StandardOutput=journal

[Install]
WantedBy=default.target
EOF

cat > ~/.config/systemd/user/desktop-monitor.timer << 'EOF'
[Unit]
Description=Desktop Health Monitor Timer
Requires=desktop-monitor.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=10min

[Install]
WantedBy=timers.target
EOF

# Enable and start the timer
systemctl --user daemon-reload
systemctl --user enable desktop-monitor.timer
systemctl --user start desktop-monitor.timer

echo ""
echo "✓ Desktop protection configured"
echo "✓ Monitoring service installed"
echo ""
echo "The system will now:"
echo "  - Check desktop health every 10 minutes"
echo "  - Auto-restart GNOME Shell if it crashes"
echo "  - Keep desktop icons enabled"
echo ""
echo "To check status:"
echo "  systemctl --user status desktop-monitor.timer"
echo ""

