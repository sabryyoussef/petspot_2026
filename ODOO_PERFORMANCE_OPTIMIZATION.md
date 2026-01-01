# Odoo Performance Optimization for 4GB RAM Ubuntu System

## Current Status Analysis

**System Memory:**
- Total: 3.8GB
- Used: 3.1GB
- Available: 739MB ⚠️ **CRITICAL - Already swapping!**
- Swap: 8GB (307MB used)

**Current Issues:**
1. ✅ Workers = 0 (already optimized)
2. ❌ PostgreSQL shared_buffers = 128MB (should be 512MB)
3. ❌ ZRAM not configured (PERCENT commented out)
4. ❌ Odoo log_level = info (should be warn)
5. ❌ High CPU/time limits (600/1200s - too high)
6. ❌ No memory limits set

---

## Optimization Implementation Guide

### 1. PostgreSQL Configuration (HIGHEST IMPACT)

**File:** `/etc/postgresql/16/main/postgresql.conf`

**Current:** `shared_buffers = 128MB`

**Recommended for 4GB RAM:**
```conf
shared_buffers = 512MB
work_mem = 16MB
maintenance_work_mem = 128MB
effective_cache_size = 2GB
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 1GB
random_page_cost = 1.1
```

**Commands:**
```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
# Add/modify the above settings
sudo systemctl restart postgresql
```

**Expected Impact:** 30-50% speedup

---

### 2. ZRAM Configuration (CRITICAL - Prevents Swap Death)

**File:** `/etc/default/zramswap`

**Current:** PERCENT is commented out

**Recommended:**
```bash
PERCENT=50
```

**Commands:**
```bash
sudo nano /etc/default/zramswap
# Uncomment and set: PERCENT=50
sudo systemctl restart zramswap
```

**Expected Impact:** Prevents PostgreSQL from being swapped → massive win

---

### 3. Odoo Configuration Optimization

#### Development Config (`odoo-dev.conf`)

**Current Issues:**
- `log_level = info` → too verbose
- `limit_time_cpu = 600` → too high
- `limit_time_real = 1200` → too high
- No memory limits

**Recommended:**
```ini
[options]
admin_passwd = admin_dev
db_host = localhost
db_port = 5432
db_user = odoo19
db_password = odoo19
db_name = petspot_dev
addons_path = /home/petspot/odoo-19/odoo19/addons,/home/petspot/odoo-19/custom_addons_dev,/home/petspot/odoo-19/custom_addons
http_port = 8070
logfile = /var/log/odoo/odoo-dev.log
log_level = warn
limit_time_cpu = 60
limit_time_real = 120
limit_memory_soft = 640000000
limit_memory_hard = 768000000
workers = 0
max_cron_threads = 1
```

#### Production Config (`odoo.conf`)

**Recommended:**
```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo19
db_password = odoo19
addons_path = /home/petspot/odoo-19/odoo19/addons,/home/petspot/odoo-19/custom_addons
http_port = 8069
http_interface = 0.0.0.0
logfile = /var/log/odoo/odoo.log
log_level = warn
limit_time_cpu = 60
limit_time_real = 120
limit_memory_soft = 640000000
limit_memory_hard = 768000000
workers = 0
max_cron_threads = 1
```

**Expected Impact:** 
- Reduced logging overhead: 5-10%
- Memory limits prevent OOM: Stability
- Lower time limits: Faster failure detection

---

### 4. PostgreSQL Index Maintenance

**Run after migrations/imports:**
```bash
sudo -u postgres psql -d petspot_dev -c "REINDEX DATABASE petspot_dev;"
sudo -u postgres psql -d petspot_dev -c "ANALYZE;"
```

**For large tables:**
```sql
VACUUM (ANALYZE);
```

**Expected Impact:** 10-30% query speedup

---

### 5. Disable Unused Features

**If not using email polling:**
```ini
# In odoo.conf
# fetchmail_cron = False  # Uncomment if not using
```

**If not using longpolling:**
```ini
# longpolling_port = False  # Uncomment if not using
```

---

### 6. System Dependencies Check

**Already Installed:**
- ✅ libpq-dev
- ✅ libpq5
- ✅ Python 3.12.3 (good version)

**Verify psycopg2:**
```bash
python3 -c "import psycopg2; print(psycopg2.__version__)"
```

If missing:
```bash
pip install psycopg2-binary
```

---

## Implementation Priority

| Priority | Action | Impact | Time |
|----------|--------|--------|------|
| 🔥🔥🔥🔥 | PostgreSQL tuning | 30-50% | 5 min |
| 🔥🔥🔥 | ZRAM configuration | Prevents swap | 2 min |
| 🔥🔥🔥 | Odoo memory limits | Stability | 2 min |
| 🔥🔥 | Log level reduction | 5-10% | 1 min |
| 🔥🔥 | Index maintenance | 10-30% | 10 min |

---

## Verification Commands

**Check memory after optimization:**
```bash
free -h
htop
```

**Check PostgreSQL settings:**
```bash
sudo -u postgres psql -c "SHOW shared_buffers;"
sudo -u postgres psql -c "SHOW work_mem;"
```

**Check Odoo memory usage:**
```bash
ps aux | grep odoo-bin | awk '{print $6/1024 " MB"}'
```

**Monitor slow queries:**
```bash
# Temporarily enable in postgresql.conf:
# log_min_duration_statement = 500
# Then check: /var/log/postgresql/postgresql-16-main.log
```

---

## Expected Results

**Before:**
- Available RAM: 739MB
- Already swapping: Yes
- PostgreSQL shared_buffers: 128MB
- No memory limits

**After:**
- Available RAM: ~1.5GB (with ZRAM)
- Swapping: Reduced/minimal
- PostgreSQL shared_buffers: 512MB
- Memory limits: Enforced
- **Overall speedup: 40-60%**

---

## Notes

- **Two Odoo instances running** - Consider if both are needed
- **Memory is critical** - Monitor closely after changes
- **Restart services** after PostgreSQL changes
- **Test thoroughly** after optimizations

---

## Rollback Plan

If issues occur:
1. Revert PostgreSQL config: `sudo systemctl restart postgresql`
2. Revert Odoo config: Restart Odoo
3. Disable ZRAM: `sudo systemctl stop zramswap`

