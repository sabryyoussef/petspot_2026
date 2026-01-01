# POS Cashout to Expense - Testing Guide

## ✅ Module Restart Complete

**Date:** 2025-12-22  
**Status:** Odoo dev restarted successfully (PID: 36028)  
**Server:** http://192.168.100.64:8070  
**Module:** pos_cashout_expense

---

## 🧪 Testing Steps

### Step 1: Open POS
1. Go to http://192.168.100.64:8070
2. Log in to Odoo
3. Open **Point of Sale** app
4. Open a session (if not already open)

### Step 2: Make a Cash Out
1. In POS, click the **menu** (three dots or hamburger icon)
2. Select **Cash In/Out**
3. Select **Cash Out** tab
4. Enter amount: `1000` (or any amount)
5. Enter reason: `Test expense` (or any reason)
6. Click **Confirm** button
   - ✅ You should see success message
   - ✅ Popup should **stay open** (not close)
   - ✅ "Add to Expense" button should appear and be **enabled** (blue/primary color)

### Step 3: Create Expense
1. Click **"Add to Expense"** button
   - ✅ A **new browser window/tab** should open
   - ✅ You should see the **Expense form** with:
     - Name: Your reason (e.g., "Test expense")
     - Amount: The cash out amount (e.g., 1000)
     - Employee: Current user's employee
     - State: Draft

2. In the expense form:
   - Add more details if needed (category, notes, etc.)
   - Click **Save** to save the draft expense
   - Or click **Submit to Manager** to submit it

### Step 4: Verify in Expenses Module
1. Go back to Odoo backend
2. Open **Expenses** app
3. Go to **My Expenses** → **My Expenses to Submit**
4. You should see your expense listed there

---

## ⚠️ Troubleshooting

### If "Add to Expense" button doesn't appear:
- Make sure you clicked **Confirm** first (cash out must be confirmed)
- Check browser console for JavaScript errors (F12)
- Refresh POS and try again

### If button is disabled (gray):
- The button only enables after clicking Confirm
- Wait a moment after clicking Confirm

### If expense form doesn't open:
- Check if popup blocker is enabled - disable it for this site
- Check browser console for errors
- Check `/var/log/odoo/odoo-dev.log` for Python errors

### If you get "method does not exist" error:
- The module wasn't fully loaded yet
- Check logs: `tail -50 /var/log/odoo/odoo-dev.log`
- May need another restart

---

## 🔧 Technical Details

### What Changed:
1. **Frontend (`cash_move_popup.js`):**
   - Patched `CashMovePopup` to keep popup open after cash out
   - Added `openExpenseForm()` method
   - Tracks cash out confirmation state

2. **Frontend (`cash_move_popup.xml`):**
   - Added "Add to Expense" button (visible only for cash out)
   - Button enables after confirm

3. **Backend (`pos_session.py`):**
   - Added `prepare_expense_from_cashout()` method
   - Creates draft expense from cash out
   - Links expense to statement line

4. **Backend (`hr_expense.py`):**
   - Added `pos_statement_line_id` field to track POS link

---

## 📝 Expected Behavior

### Flow:
1. User makes cash out → clicks Confirm
2. Cash is withdrawn from register
3. Popup stays open, "Add to Expense" button appears
4. User clicks "Add to Expense"
5. Expense form opens in new window
6. User completes expense details
7. Expense is saved/submitted

### Benefits:
- Quick expense creation from POS
- Automatic linking to cash movement
- Traceability between POS and Expenses
- No manual data entry needed

---

## ✨ Module Ready for Testing!

Python cache cleared ✅  
Odoo restarted ✅  
Module loaded ✅  
Ready to test ✅

