#!/bin/bash
# Quick check script for pos_cashout_expense module

echo "=========================================="
echo "POS Cashout Expense Module Check"
echo "=========================================="
echo ""

echo "1. Checking if module files exist..."
if [ -f "/home/petspot/odoo-19/custom_addons_dev/pos_cashout_expense/__manifest__.py" ]; then
    echo "   ✓ Module directory exists"
else
    echo "   ✗ Module directory NOT found"
    exit 1
fi

echo ""
echo "2. Checking module files..."
FILES=(
    "__manifest__.py"
    "__init__.py"
    "models/__init__.py"
    "models/pos_session.py"
    "models/hr_expense.py"
    "static/src/js/cash_move_popup.js"
    "static/src/xml/cash_move_popup.xml"
    "security/ir.model.access.csv"
)

for file in "${FILES[@]}"; do
    if [ -f "/home/petspot/odoo-19/custom_addons_dev/pos_cashout_expense/$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file MISSING"
    fi
done

echo ""
echo "3. Checking manifest asset bundle..."
if grep -q "point_of_sale._assets_pos" /home/petspot/odoo-19/custom_addons_dev/pos_cashout_expense/__manifest__.py; then
    echo "   ✓ Asset bundle is correct: point_of_sale._assets_pos"
else
    echo "   ✗ Asset bundle is WRONG"
fi

echo ""
echo "4. Checking if module is in addons path..."
if grep -q "custom_addons_dev" /home/petspot/odoo-19/odoo-conf/odoo-dev.conf; then
    echo "   ✓ custom_addons_dev is in addons path"
else
    echo "   ✗ custom_addons_dev NOT in addons path"
fi

echo ""
echo "5. Module installation status..."
echo "   To check if module is installed, run in Odoo:"
echo "   - Go to Apps menu"
echo "   - Search for 'POS Cashout to Expense'"
echo "   - Check if it shows 'Installed'"
echo ""
echo "6. Next steps if button not appearing:"
echo "   1. Upgrade the module in Odoo Apps menu"
echo "   2. Clear browser cache (Ctrl+Shift+R)"
echo "   3. Restart Odoo"
echo "   4. Check browser console (F12) for errors"
echo ""

