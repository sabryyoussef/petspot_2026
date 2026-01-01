# PetSpot Odoo 19 Instance

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-714B67?style=flat-square&logo=odoo)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16.11-336791?style=flat-square&logo=postgresql)

Enterprise Odoo 19 instance for PetSpot veterinary practice management with custom modules, automated backups, and sync tools.

## 🌐 Live Instance
- **Production**: https://vetdrughouse.ddns.net/odoo
- **Database**: `petspot` (port 8069)
- **Development**: `petspot_dev` (port 8070)

## 📦 Features

### Custom Modules
- **POS Point of Sale** with custom cashout and expense tracking
- **Desktop Integration** for local operations
- **Product Management** for veterinary supplies
- **HR & Employee Management** 
- **CRM & Sales**
- **Inventory & Stock Management**

### Automation Tools

#### 🔄 Database Backup System
- **Location**: `/home/petspot/Dropbox/odoo_backups/`
- **Schedule**: Daily at 2:00 AM
- **Format**: PostgreSQL custom format (-Fc) with compression
- **Retention**: 7 days (auto-cleanup)
- **Verification**: Automatic integrity checks after each backup

#### 🔁 Instance Sync Tool
- **Direction**: Production → Development
- **Mode**: 
  - First run: Full sync
  - Subsequent: Incremental (only new/updated records)
- **State Tracking**: ID mappings and sync history
- **Models**: Partners, Products, Sales, Invoices, HR, Projects, etc.

## 🚀 Quick Start

### Prerequisites
```bash
# Ubuntu 24.04
sudo apt update
sudo apt install python3 python3-pip postgresql-16 nginx
```

### Installation
```bash
# Clone the repository
git clone git@github.com:sabryyoussef/petspot_2026.git
cd petspot_2026

# Install Odoo dependencies
pip3 install -r requirements.txt

# Run production instance
./INSTALL_PRODUCTION.sh
```

## 📁 Repository Structure

```
petspot_2026/
├── odoo19/                      # Odoo 19 core
├── custom_addons/               # Production custom modules
├── custom_addons_dev/           # Development custom modules
├── odoo-conf/                   # Configuration files
│   ├── odoo.conf               # Production config (port 8069)
│   └── odoo-dev.conf           # Development config (port 8070)
├── odoo_sync.py                # Database sync tool
├── backup_database.py          # Automated backup script
├── BACKUP_README.md            # Backup documentation
├── SYNC_README.md              # Sync tool documentation
└── *.md                        # Various guides and docs
```

## 🛠️ Configuration

### Production Instance
- **Port**: 8069
- **Database**: petspot
- **Addons**: `/home/petspot/odoo-19/odoo19/addons,/home/petspot/odoo-19/custom_addons`
- **Log**: `/var/log/odoo/odoo.log`

### Development Instance
- **Port**: 8070
- **Database**: petspot_dev
- **Addons**: `/home/petspot/odoo-19/odoo19/addons,/home/petspot/odoo-19/custom_addons_dev,/home/petspot/odoo-19/custom_addons`
- **Log**: `/var/log/odoo/odoo-dev.log`

## 🔧 Management Commands

### Database Operations
```bash
# Backup databases manually
python3 backup_database.py

# Sync production to development
python3 odoo_sync.py

# View backup logs
cat backup.log

# List all backups
ls -lh ~/Dropbox/odoo_backups/
```

### Odoo Service Management
```bash
# Check running instances
ps aux | grep odoo

# View production logs
tail -f /var/log/odoo/odoo.log

# View development logs
tail -f /var/log/odoo/odoo-dev.log
```

### Database Restore
```bash
# Restore from backup
pg_restore -U odoo19 -d petspot_dev ~/Dropbox/odoo_backups/petspot_YYYY-MM-DD_HHMM.dump

# Verify backup integrity
pg_restore -l ~/Dropbox/odoo_backups/petspot_*.dump | head
```

## 📊 Monitoring

### Backup Status
- Backups stored in Dropbox (auto-synced to cloud)
- Automatic verification after each backup
- Email notifications on failure (configurable)

### Sync Status
- Sync state tracked in `sync_state.json`
- ID mappings preserved between instances
- Incremental sync for efficiency

## 🔐 Security

- PostgreSQL credentials in `~/.pgpass` (mode 600)
- API keys stored securely in database
- Admin passwords: Change default credentials!
- Firewall configured for ports 8069/8070

## 📚 Documentation

- [Backup System Guide](BACKUP_README.md)
- [Sync Tool Guide](SYNC_README.md)
- [Module Installation](INSTALL_MODULE_UI.md)
- [Performance Optimization](ODOO_PERFORMANCE_OPTIMIZATION.md)
- [Production Deployment](PRODUCTION_DEPLOYMENT.md)
- [SSH Setup](SETUP_SSH_PASSWORDLESS.md)
- [Desktop Protection](DESKTOP_PROTECTION_GUIDE.md)

## 🏗️ Development

### Branches
- **main**: Production-ready code
- **dev**: Development and testing

### Adding Custom Modules
```bash
# Create new module
cd custom_addons_dev
mkdir my_module
cd my_module
# Create __manifest__.py and module files

# Restart Odoo
# Access http://localhost:8070 and activate developer mode
```

### Testing Changes
1. Develop in `custom_addons_dev`
2. Test on development instance (port 8070)
3. Sync from production to dev for latest data
4. Move stable modules to `custom_addons`
5. Deploy to production

## 🤝 Contributing

This is a private repository for PetSpot veterinary practice.

## 📝 License

Proprietary - PetSpot 2026

## 👥 Contact

**Sabry Youssef**  
- GitHub: [@sabryyoussef](https://github.com/sabryyoussef)
- Email: sabry@petspot.com

---

## 🔄 Recent Updates

### January 2026
- ✅ Automated daily backups to Dropbox
- ✅ Production to development sync tool
- ✅ Custom POS cashout module
- ✅ Desktop integration improvements
- ✅ Performance optimizations
- ✅ Documentation updates

## 📈 Statistics

- **Databases**: 2 (Production + Dev)
- **Custom Modules**: 15+
- **Active Users**: 6
- **Backup Size**: ~28 MB compressed (both DBs)
- **Sync Time**: ~5 minutes (incremental)

---

**Built with ❤️ for PetSpot Veterinary Practice**

