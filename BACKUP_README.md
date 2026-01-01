# Odoo Database Backup System

## Overview
Automated daily backup system for Odoo databases to Dropbox folder.
- **Databases**: `petspot` and `petspot_dev`
- **Backup Location**: `/home/petspot/Dropbox/odoo_backups/`
- **Schedule**: Twice daily at 1:00 PM and 10:00 PM (during business hours)
- **Retention**: 7 days (older backups automatically deleted)

## Files Created

### Backup Script
- **`backup_database.py`** - Main backup script
  - Uses PostgreSQL custom format (`pg_dump -Fc`) with built-in compression
  - Verifies backup integrity after creation
  - Automatic cleanup of old backups
  - Detailed logging

### Configuration Files
- **`~/.pgpass`** - PostgreSQL authentication (secure, mode 600)
  - Format: `localhost:5432:*:odoo19:odoo19`

### Logs
- **`backup.log`** - Complete backup history
- **`backup_cron.log`** - Output from cron job executions

## Current Status

### ✅ Successfully Configured
- Backup script tested and working
- Both databases backed up successfully
- Dumps verified (18,713 and 18,729 TOC entries)
- Cron job scheduled
- Backup rotation enabled (keeps 7 days)

### Latest Backups
```bash
petspot_2026-01-01_1707.dump          16M  (18,713 TOC entries)
petspot_dev_2026-01-01_1707.dump      12M  (18,729 TOC entries)
```

## Usage

### Manual Backup
Run the backup script manually at any time:
```bash
cd /home/petspot/odoo-19
python3 backup_database.py
```

### View Backup Logs
```bash
# Full backup history
cat /home/petspot/odoo-19/backup.log

# Cron job logs
cat /home/petspot/odoo-19/backup_cron.log
```

### List All Backups
```bash
ls -lh ~/Dropbox/odoo_backups/
```

### Verify a Backup
Check backup integrity and contents:
```bash
# List TOC entries (first 20 lines)
pg_restore -l ~/Dropbox/odoo_backups/petspot_*.dump | head -20

# Get specific backup
pg_restore -l ~/Dropbox/odoo_backups/petspot_2026-01-01_1707.dump | head
```

## Restoring a Database

### Full Database Restore
```bash
# Drop and recreate database (CAUTION!)
dropdb -U odoo19 petspot_test
createdb -U odoo19 petspot_test

# Restore from backup
pg_restore -U odoo19 -d petspot_test ~/Dropbox/odoo_backups/petspot_2026-01-01_1707.dump
```

### Restore Specific Tables
```bash
# List available tables
pg_restore -l ~/Dropbox/odoo_backups/petspot_2026-01-01_1707.dump | grep TABLE

# Restore specific table
pg_restore -U odoo19 -d petspot -t res_partner ~/Dropbox/odoo_backups/petspot_2026-01-01_1707.dump
```

## Backup Schedule

### Current Schedule
The backup runs automatically twice daily during business hours:
- **1:00 PM (13:00)** - Beginning of business day
- **10:00 PM (22:00)** - End of business day
- **All databases**: petspot, petspot_dev

### View Cron Schedule
```bash
crontab -l
```

### Change Backup Time
Edit the crontab:
```bash
crontab -e
```

Cron time format: `minute hour day month weekday`
- Current setting (1 PM & 10 PM): `0 13 * * *` and `0 22 * * *`
- Once at 2 PM: `0 14 * * *`
- Three times (1 PM, 5 PM, 10 PM): `0 13,17,22 * * *`
- Every 3 hours during business (1 PM, 4 PM, 7 PM, 10 PM): `0 13,16,19,22 * * *`

## Backup Configuration

### Change Retention Period
Edit `/home/petspot/odoo-19/backup_database.py`:
```python
CONFIG = {
    ...
    'keep_days': 7,  # Change this number
    ...
}
```

### Add/Remove Databases
Edit the databases list in `backup_database.py`:
```python
CONFIG = {
    'databases': ['petspot', 'petspot_dev', 'another_db'],  # Add more here
    ...
}
```

## Troubleshooting

### Check if Cron Service is Running
```bash
systemctl status cron
```

### Test Backup Manually
```bash
cd /home/petspot/odoo-19
python3 backup_database.py
```

### Check Disk Space in Dropbox
```bash
df -h ~/Dropbox/
du -sh ~/Dropbox/odoo_backups/
```

### PostgreSQL Connection Issues
Verify `.pgpass` file:
```bash
cat ~/.pgpass
# Should show: localhost:5432:*:odoo19:odoo19

# Check permissions (must be 600)
ls -l ~/.pgpass
```

### View Backup Statistics
The script shows statistics after each run:
- Number of backups per database
- Total size
- Latest backup time

## Backup File Format

### Naming Convention
```
{database}_{YYYY-MM-DD}_{HHMM}.dump
```
Examples:
- `petspot_2026-01-01_0200.dump`
- `petspot_dev_2026-01-01_0200.dump`

### Format Details
- **Type**: PostgreSQL custom archive format
- **Compression**: Built-in gzip compression
- **Verification**: Automatically verified after creation
- **Typical Size**:
  - petspot: ~16 MB compressed
  - petspot_dev: ~12 MB compressed

## Automatic Cleanup

The script automatically:
1. Keeps backups for the last 7 days
2. Deletes older backups during each run
3. Logs all deletions

### Manual Cleanup
To remove old backups manually:
```bash
# Delete backups older than 7 days
find ~/Dropbox/odoo_backups/ -name "*.dump" -mtime +7 -delete

# Keep only last 3 backups per database
cd ~/Dropbox/odoo_backups/
ls -t petspot_*.dump | tail -n +4 | xargs rm -f
ls -t petspot_dev_*.dump | tail -n +4 | xargs rm -f
```

## Disaster Recovery

### Quick Recovery Steps
1. **Identify the backup to restore**:
   ```bash
   ls -lht ~/Dropbox/odoo_backups/ | head
   ```

2. **Stop Odoo services**:
   ```bash
   # Stop both instances if restoring production
   sudo systemctl stop odoo
   ```

3. **Restore database**:
   ```bash
   pg_restore -U odoo19 -d petspot --clean ~/Dropbox/odoo_backups/petspot_YYYY-MM-DD_HHMM.dump
   ```

4. **Start Odoo services**:
   ```bash
   sudo systemctl start odoo
   ```

## Security Notes

- `.pgpass` file has secure permissions (600) - only you can read it
- Backups contain sensitive data - keep Dropbox secure
- Backups are compressed but not encrypted
- Consider encrypting backups for compliance requirements

## Monitoring

### Check Last Backup Time
```bash
ls -lt ~/Dropbox/odoo_backups/ | head -3
```

### Verify Backup is Running Daily
```bash
# Check cron log for today's backup
tail -50 /home/petspot/odoo-19/backup_cron.log
```

### Check Backup Sizes
```bash
du -sh ~/Dropbox/odoo_backups/*
```

## Advanced: Offsite Backup

Since backups are in Dropbox, they're automatically:
- ✅ Synchronized to cloud
- ✅ Available on all devices with Dropbox
- ✅ Protected with Dropbox's versioning
- ✅ Can be shared with team members (if needed)

Dropbox keeps deleted files for 30 days (or longer with Dropbox Business).

---
**Created**: January 2026  
**PostgreSQL Version**: 16.11  
**Odoo Version**: 19.0  
**Python**: 3.x (uses built-in libraries)

