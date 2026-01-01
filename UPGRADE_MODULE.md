# Module Upgrade Required

## Issue
The `pos_cashout_expense` module has been updated with a new method `prepare_expense_from_cashout`, but Odoo hasn't loaded it yet.

## Error
```
AttributeError: The method 'pos.session.prepare_expense_from_cashout' does not exist
```

## Solution: Upgrade the Module

### Option 1: Via Odoo UI (Recommended)
1. Go to Odoo backend (not POS): `http://192.168.100.64:8070`
2. Go to **Apps** menu
3. Remove the "Apps" filter (click the X on the search bar)
4. Search for "**pos_cashout_expense**" or "**POS Cashout to Expense**"
5. Click the **Upgrade** button (three dots menu → Upgrade)

### Option 2: Restart Odoo in PyCharm
Since you manage Odoo through PyCharm:
1. Stop the Odoo process in PyCharm
2. Start it again

The Python cache has been cleared, so after restart, the new method will be loaded.

## What Was Changed
- Added method `prepare_expense_from_cashout` in `custom_addons_dev/pos_cashout_expense/models/pos_session.py`
- This method creates a draft expense and returns the expense ID
- The frontend calls this method when you click "Add to Expense"

## After Upgrade
1. Go back to POS
2. Make a cash out
3. Click "Confirm"
4. Click "Add to Expense" button (should be enabled now)
5. The expense form should open in a new window/tab

## Status
✅ Python cache cleared
⏳ Waiting for module upgrade or Odoo restart

