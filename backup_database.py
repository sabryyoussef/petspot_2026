#!/usr/bin/env python3
"""
Odoo Database Backup Script
Automatically backs up Odoo databases to Dropbox folder
- PostgreSQL custom format (-Fc) with built-in compression
- Automatic rotation (keeps last 7 days)
- Logs all operations
"""

import subprocess
import os
from datetime import datetime, timedelta
import glob
import sys

# Configuration
CONFIG = {
    'databases': ['petspot', 'petspot_dev'],  # Databases to backup
    'backup_dir': '/home/petspot/Dropbox/odoo_backups',
    'temp_dir': '/tmp',
    'keep_days': 7,  # Number of days to keep backups
    'log_file': '/home/petspot/odoo-19/backup.log'
}


def log_message(message):
    """Log message to console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    
    try:
        with open(CONFIG['log_file'], 'a') as f:
            f.write(log_line + '\n')
    except Exception as e:
        print(f"Warning: Could not write to log file: {e}")


def ensure_backup_directory():
    """Create backup directory if it doesn't exist"""
    backup_dir = CONFIG['backup_dir']
    
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
            log_message(f"✅ Created backup directory: {backup_dir}")
        except Exception as e:
            log_message(f"❌ Error creating backup directory: {e}")
            return False
    
    return True


def backup_database(db_name):
    """Backup a single database using pg_dump custom format"""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    backup_filename = f"{db_name}_{timestamp}.dump"
    final_path = os.path.join(CONFIG['backup_dir'], backup_filename)
    
    log_message(f"📦 Starting backup of database: {db_name}")
    
    # Construct pg_dump command with custom format (-Fc) and built-in compression
    # Write directly to final destination
    pg_dump_cmd = [
        'pg_dump',
        '-U', 'odoo19',  # PostgreSQL user
        '-h', 'localhost',  # Host
        '-Fc',  # Custom format with compression
        '-d', db_name,
        '-f', final_path
    ]
    
    try:
        # Run pg_dump
        log_message(f"   Running pg_dump for {db_name}...")
        
        result = subprocess.run(
            pg_dump_cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            log_message(f"❌ pg_dump failed for {db_name}")
            if result.stderr:
                log_message(f"   Error: {result.stderr}")
            if os.path.exists(final_path):
                os.remove(final_path)
            return False
        
        # Check if backup file was created
        if not os.path.exists(final_path):
            log_message(f"❌ Backup file was not created: {final_path}")
            return False
        
        # Verify final file
        file_size = os.path.getsize(final_path)
        file_size_mb = file_size / (1024 * 1024)
        log_message(f"✅ Backup completed: {backup_filename} ({file_size_mb:.2f} MB)")
        
        # Verify dump integrity
        verify_cmd = ['pg_restore', '-l', final_path]
        verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
        
        if verify_result.returncode == 0:
            toc_lines = verify_result.stdout.split('\n')
            toc_count = len([l for l in toc_lines if l and not l.startswith(';')])
            log_message(f"   ✓ Dump verified: {toc_count} TOC entries")
        else:
            log_message(f"   ⚠ Warning: Could not verify dump integrity")
        
        return True
            
    except Exception as e:
        log_message(f"❌ Error backing up {db_name}: {e}")
        if os.path.exists(final_path):
            try:
                os.remove(final_path)
            except:
                pass
        return False


def cleanup_old_backups():
    """Remove backups older than keep_days"""
    log_message(f"🧹 Cleaning up backups older than {CONFIG['keep_days']} days...")
    
    cutoff_date = datetime.now() - timedelta(days=CONFIG['keep_days'])
    backup_dir = CONFIG['backup_dir']
    
    deleted_count = 0
    kept_count = 0
    
    for db_name in CONFIG['databases']:
        pattern = os.path.join(backup_dir, f"{db_name}_*.dump")
        backup_files = glob.glob(pattern)
        
        for backup_file in backup_files:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(backup_file))
                
                if file_time < cutoff_date:
                    os.remove(backup_file)
                    deleted_count += 1
                    log_message(f"   Deleted old backup: {os.path.basename(backup_file)}")
                else:
                    kept_count += 1
            except Exception as e:
                log_message(f"   Warning: Could not process {backup_file}: {e}")
    
    log_message(f"✅ Cleanup complete: Deleted {deleted_count}, Kept {kept_count}")


def get_backup_statistics():
    """Display backup statistics"""
    log_message("📊 Backup Statistics:")
    
    backup_dir = CONFIG['backup_dir']
    total_size = 0
    
    for db_name in CONFIG['databases']:
        pattern = os.path.join(backup_dir, f"{db_name}_*.dump")
        backup_files = sorted(glob.glob(pattern))
        
        if backup_files:
            db_size = sum(os.path.getsize(f) for f in backup_files)
            total_size += db_size
            
            latest_backup = backup_files[-1]
            latest_time = datetime.fromtimestamp(os.path.getmtime(latest_backup))
            
            log_message(f"   {db_name}:")
            log_message(f"      Total backups: {len(backup_files)}")
            log_message(f"      Total size: {db_size / (1024*1024):.2f} MB")
            log_message(f"      Latest: {os.path.basename(latest_backup)} ({latest_time.strftime('%Y-%m-%d %H:%M')})")
        else:
            log_message(f"   {db_name}: No backups found")
    
    log_message(f"   Total size all backups: {total_size / (1024*1024):.2f} MB")


def main():
    """Main backup execution"""
    log_message("="*60)
    log_message("🚀 ODOO DATABASE BACKUP STARTED")
    log_message("="*60)
    
    # Ensure backup directory exists
    if not ensure_backup_directory():
        log_message("❌ Cannot proceed without backup directory")
        sys.exit(1)
    
    # Backup each database
    success_count = 0
    fail_count = 0
    
    for db_name in CONFIG['databases']:
        if backup_database(db_name):
            success_count += 1
        else:
            fail_count += 1
    
    # Cleanup old backups
    cleanup_old_backups()
    
    # Show statistics
    get_backup_statistics()
    
    # Summary
    log_message("="*60)
    log_message(f"✅ BACKUP COMPLETE: {success_count} successful, {fail_count} failed")
    log_message("="*60)
    
    if fail_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

