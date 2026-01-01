# POS Cashout to Expense - Production Deployment

## ✅ Module Copied to Production

**Date:** 2025-12-22  
**Module:** pos_cashout_expense  
**Source:** `/home/petspot/odoo-19/custom_addons_dev/pos_cashout_expense`  
**Production:** `/home/petspot/odoo-19/custom_addons/pos_cashout_expense`  
**Status:** Ready for production deployment

---

## 📦 Module Structure

```
custom_addons/pos_cashout_expense/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── pos_session.py       # Backend: prepare_expense_from_cashout()
│   └── hr_expense.py         # Backend: pos_statement_line_id field
├── security/
│   └── ir.model.access.csv   # Access rights
└── static/
    └── src/
        ├── js/
        │   └── cash_move_popup.js    # Frontend: button logic
        └── xml/
            └── cash_move_popup.xml    # Frontend: button template
```

---

## 🚀 Production Deployment Steps

### Step 1: Install Module on Production Server

**If using production config (port 8069):**

1. Go to production Odoo: **http://192.168.100.64:8069**
2. Log in with admin credentials
3. Go to **Apps** menu
4. Click **Update Apps List** (to scan for new modules)
5. Remove "Apps" filter (click X on search bar)
6. Search for "**pos_cashout_expense**" or "**POS Cashout to Expense**"
7. Click **Install**

**Alternative: Command Line Installation**
```bash
cd /home/petspot/odoo-19
python3 odoo19/odoo-bin -c odoo-conf/odoo.conf -d petspot -i pos_cashout_expense --stop-after-init
```

### Step 2: Verify Installation

1. Check installed modules:
   - Apps → Search "pos_cashout_expense"
   - Status should be "Installed"

2. Check access rights:
   - Settings → Users & Companies → Groups
   - Verify POS users have access

3. Test basic functionality:
   - Open POS on production
   - Make a test cash out
   - Verify button appears

---

## ⚙️ Configuration

### Required Modules
The following modules must be installed on production:
- ✅ `point_of_sale` (POS)
- ✅ `hr_expense` (Expenses)

### Required Setup
1. **Employee Records:**
   - Each POS user must have an employee record
   - Link: Settings → Users → User → HR Settings → Related Employee

2. **Expense Products:**
   - At least one product with "Can be Expensed" enabled
   - Create one: Expenses → Configuration → Expense Products

3. **Access Rights:**
   - Pthree POS users should have expense creation rights
   - Settings → Users → User → Access Rights → Expenses: User (All Documents)

---

## 🔧 Production Server Info

### Port 8069 (Production)
```ini
Config: /home/petspot/odoo-19/odoo-conf/odoo.conf
Addons: /home/petspot/odoo-19/custom_addons
Database: petspot (main production DB)
Log: /var/log/odoo/odoo.log
```

### Port 8070 (Development - Already Tested)
```ini
Config: /home/petspot/odoo-19/odoo-conf/odoo-dev.conf
Addons: /home/petspot/odoo-19/custom_addons_dev
Database: petspot_dev
Log: /var/log/odoo/odoo-dev.log
Status: ✅ Tested and working
```

---

## 🧪 Production Testing Checklist

After installation on production:

- [ ] Module appears in Apps list
- [ ] Module status shows "Installed"
- [ ] Open POS interface
- [ ] Start/open a session
- [ ] Click Cash In/Out → Cash Out
- [ ] Enter test amount and reason
- [ ] Click Confirm
- [ ] Verify popup stays open
- [ ] Verify "Add to Expense" button appears
- [ ] Click "Add to Expense" button
- [ ] Verify expense form opens in new window
- [ ] Verify expense has correct amount and reason
- [ ] Save/submit expense
- [ ] Check expense in Expenses module
- [ ] Verify expense is linked to POS session

---

## 📊 Monitoring

### Check Logs
```bash
# Production logs
tail -f /var/log/odoo/odoo.log | grep -E "pos_cashout_expense|prepare_expense|ERROR"

# Development logs (already working)
tail -f /var/log/odoo/odoo-dev.log | grep -E "pos_cashout_expense|prepare_expense|ERROR"
```

### Common Issues

**Issue: Module not found**
- Solution: Update Apps List in Odoo

**Issue: Method does not exist**
- Solution: Restart Odoo production service or upgrade module

**Issue: Employee not found**
- Solution: Create employee record for POS user

**Issue: No expense product**
- Solution: Create an expense product with "Can be Expensed" enabled

---

## 🔄 Update Process

If you need to update the module in production:

1. Make changes in dev (`custom_addons_dev`)
2. Test thoroughly in dev (port 8070)
3. Copy to production:
   ```bash
   cp -r /home/petspot/odoo-19/custom_addons_dev/pos_cashout_expense /home/petspot/odoo-19/custom_addons/
   ```
4. Upgrade module in production Odoo:
   - Apps → pos_cashout_expense → Upgrade

---

## 📝 Version History

### v19.0.1.0.0 (Current)
- Initial release
- Add "Add to Expense" button to POS Cash Out
- Create draft expenses from POS cash out
- Link expenses to POS statement lines
- Open expense form in new window

---

## ✅ Deployment Status

- [x] Module copied to production directory
- [x] Python cache cleaned
- [x] File permissions set
- [x] Module structure verified
- [x] Development testing completed
- [ ] Production installation pending
- [ ] Production testing pending
- [ ] Production sign-off pending

---

## 🎯 Next Steps

1. **Install on Production:**
   - Update Apps List
   - Install pos_cashout_expense module

2. **Configure:**
   - Verify employee records exist
   - Verify expense products exist
   - Check user permissions

3. **Test:**
   - Follow production testing checklist
   - Test with real POS session
   - Verify expense creation workflow

4. **Go Live:**
   - Inform POS users about new feature
   - Monitor logs for any issues
   - Collect feedback

---

## 📞 Support

If issues occur in production:
1. Check `/var/log/odoo/odoo.log`
2. Verify module is installed
3. Check user permissions
4. Test in dev environment first
5. Rollback if needed (uninstall module)

Module is production-ready! ✅

