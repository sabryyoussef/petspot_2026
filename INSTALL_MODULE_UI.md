# Quick Install: POS Cashout Expense on Production

## ⚠️ Button Not Appearing - Module Not Installed Yet

The module files are copied to production, but Odoo hasn't loaded them yet.

---

## 🚀 Install Now via Odoo UI (5 Minutes)

### Step 1: Update Apps List
1. **Keep POS open** (don't close it yet)
2. Open a **new browser tab**
3. Go to: **http://192.168.100.62:8069** (or your production URL)
4. Go to **Apps** menu (top menu bar)

### Step 2: Scan for New Modules
1. Click **"Update Apps List"** button (top right area)
2. A popup will appear
3. Click **"Update"** button
4. Wait for it to finish (shows "Apps updated" message)

### Step 3: Find and Install Module
1. In the Apps screen, **remove the "Apps" filter**:
   - Click the **X** on the search filter that says "Apps"
2. In the search box, type: **`pos_cashout_expense`**
3. You should see: **"POS Cashout to Expense"** module
4. Click the **"Install"** button on the module card
5. Wait for installation (30 seconds to 1 minute)

### Step 4: Test in POS
1. Go back to your **POS tab**
2. **Refresh the POS** (press F5 or reload page)
3. Try making a cash out again:
   - Click menu → Cash In/Out
   - Cash Out tab
   - Enter amount: 1000
   - Enter reason: test
   - Click **Confirm**
   - ✅ Button "Add to Expense" should now appear!

---

## ⚡ Quick Visual Guide

```
Apps Menu → Update Apps List → Update
              ↓
Remove "Apps" Filter (click X)
              ↓
Search: "pos_cashout_expense"
              ↓
Click "Install" button
              ↓
Wait for installation
              ↓
Go back to POS → Refresh (F5)
              ↓
Test: Cash Out → Confirm → Button appears! ✅
```

---

## 🔍 Verify Installation

After installing, verify:
1. Go to **Apps** menu
2. Search: `pos_cashout_expense`
3. Status should show: **"Installed"** (green checkmark)

---

## 📝 If Module Doesn't Appear in Apps List

If after "Update Apps List" you still don't see the module:

1. Check addons path in config:
   ```bash
   grep addons_path /home/petspot/odoo-19/odoo-conf/odoo.conf
   ```
   Should show: `custom_addons`

2. Verify module files exist:
   ```bash
   ls /home/petspot/odoo-19/custom_addons/pos_cashout_expense/
   ```
   Should show: `__manifest__.py`, `models/`, `static/`, etc.

3. Restart production Odoo:
   - If running as service: `sudo systemctl restart odoo`
   - If running manually: Stop and start the process

---

## ✅ After Installation

Once installed:
- ✅ Button will appear after clicking "Confirm" on cash out
- ✅ Button opens expense form in new window
- ✅ Works exactly like in dev (port 8070)

---

**Current Status:**
- ✅ Module files copied to production
- ⏳ Module installation needed
- 🎯 Follow steps above to install

**Estimated Time:** 5 minutes

