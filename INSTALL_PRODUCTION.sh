#!/bin/bash
# Install POS Cashout to Expense module on production

echo "=========================================="
echo "Installing pos_cashout_expense on Production"
echo "=========================================="
echo ""

# Check if production server is running
if ! curl -s -o /dev/null -w "%{http_code}" http://localhost:8069 2>/dev/null | grep -q "200\|303\|302"; then
    echo "❌ Production Odoo server (port 8069) is not responding"
    echo "Please start the production server first"
    exit 1
fi

echo "✅ Production server is running on port 8069"
echo ""

# Option 1: UI Installation (Recommended)
echo "🎯 RECOMMENDED: Install via Odoo UI"
echo "=================================="
echo "1. Go to: http://192.168.100.64:8069"
echo "2. Log in with admin credentials"
echo "3. Go to: Apps menu"
echo "4. Click: 'Update Apps List' button"
echo "5. Remove 'Apps' filter (click X)"
echo "6. Search: 'pos_cashout_expense'"
echo "7. Click: 'Install' button"
echo ""

# Option 2: Command Line Installation
echo "📝 ALTERNATIVE: Install via Command Line"
echo "========================================"
echo "Run this command:"
echo ""
echo "cd /home/petspot/odoo-19 && python3 odoo19/odoo-bin -c odoo-conf/odoo.conf -d petspot -i pos_cashout_expense --stop-after-init"
echo ""
echo "Note: This will temporarily stop production Odoo"
echo ""

# Module info
echo "📦 Module Information"
echo "===================="
echo "Name: POS Cashout to Expense"
echo "Technical Name: pos_cashout_expense"
echo "Version: 19.0.1.0.0"
echo "Location: /home/petspot/odoo-19/custom_addons/pos_cashout_expense"
echo "Depends on: point_of_sale, hr_expense"
echo ""

echo "✅ Module is ready for production installation!"
echo ""
echo "For detailed instructions, see: PRODUCTION_DEPLOYMENT.md"

