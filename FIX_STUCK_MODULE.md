# Fix Stuck Module Upgrade

## Problem
Module "POS Cashout to Expense" stuck in "Upgrading" state

## Quick Fix

### Step 1: Refresh the Apps Page
1. **Press F5** (or Ctrl+R) on the Apps page
2. Check if module status changed

### Step 2: If Still Stuck - Reset Module State
The module state has been reset in the database.

### Step 3: Install Fresh
1. Search for: **`pos_cashout_expense`**
2. If it shows "Uninstalled" or no status, click **"Install"**
3. If it still shows "Upgrading", close your browser and reopen
4. Go back to Apps and try again

---

## Alternative: Manual Reset (if above doesn't work)

If the module is still stuck after refreshing:

1. **Close POS completely** (close that browser tab)
2. **Refresh Apps page** (F5)
3. The module should now show as ready to install
4. Click **"Install"**
5. Wait for installation to complete
6. Go back to POS and test

---

## What I Did
- Reset module state in database from "upgrading" to "uninstalled"
- Cleared any stuck installation locks
- Module is now ready for fresh installation

---

## Next Steps
1. **Refresh this page** (F5)
2. Module should appear as ready to install
3. Click **"Install"**
4. Should complete in 30 seconds
5. Then test in POS

If you still see "Upgrading" after refreshing, it means the browser cache is stuck. Close the browser completely and reopen.

