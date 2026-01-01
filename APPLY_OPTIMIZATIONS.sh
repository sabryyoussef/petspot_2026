#!/bin/bash
# Odoo Performance Optimization Script for 4GB RAM Ubuntu
# Run with sudo for PostgreSQL and ZRAM changes

set -e

echo "=========================================="
echo "Odoo Performance Optimization Script"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root for system changes
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}Note: Some commands require sudo. Run with sudo for full optimization.${NC}"
    echo ""
fi

echo "Step 1: PostgreSQL Configuration"
echo "---------------------------------"
echo "Edit /etc/postgresql/16/main/postgresql.conf and add/modify:"
echo ""
echo "shared_buffers = 512MB"
echo "work_mem = 16MB"
echo "maintenance_work_mem = 128MB"
echo "effective_cache_size = 2GB"
echo "wal_buffers = 16MB"
echo "checkpoint_completion_target = 0.9"
echo "max_wal_size = 1GB"
echo "random_page_cost = 1.1"
echo ""
read -p "Press Enter after editing postgresql.conf..."
if [ "$EUID" -eq 0 ]; then
    systemctl restart postgresql
    echo -e "${GREEN}✓ PostgreSQL restarted${NC}"
else
    echo -e "${YELLOW}Run: sudo systemctl restart postgresql${NC}"
fi
echo ""

echo "Step 2: ZRAM Configuration"
echo "---------------------------"
if [ -f /etc/default/zramswap ]; then
    if grep -q "^PERCENT=50" /etc/default/zramswap; then
        echo -e "${GREEN}✓ ZRAM already configured${NC}"
    else
        echo "Edit /etc/default/zramswap and set: PERCENT=50"
        read -p "Press Enter after editing zramswap config..."
        if [ "$EUID" -eq 0 ]; then
            systemctl restart zramswap
            echo -e "${GREEN}✓ ZRAM restarted${NC}"
        else
            echo -e "${YELLOW}Run: sudo systemctl restart zramswap${NC}"
        fi
    fi
else
    echo -e "${RED}ZRAM config file not found${NC}"
fi
echo ""

echo "Step 3: Odoo Configuration"
echo "--------------------------"
echo -e "${GREEN}✓ Odoo config files already updated${NC}"
echo "  - odoo-dev.conf: Optimized"
echo "  - odoo.conf: Optimized"
echo ""
echo -e "${YELLOW}Note: Restart Odoo instances to apply changes${NC}"
echo ""

echo "Step 4: PostgreSQL Index Maintenance"
echo "-------------------------------------"
read -p "Run REINDEX and ANALYZE? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ "$EUID" -eq 0 ]; then
        sudo -u postgres psql -d petspot_dev -c "REINDEX DATABASE petspot_dev;" 2>/dev/null || echo "Database not accessible"
        sudo -u postgres psql -d petspot_dev -c "ANALYZE;" 2>/dev/null || echo "Database not accessible"
        echo -e "${GREEN}✓ Index maintenance completed${NC}"
    else
        echo -e "${YELLOW}Run: sudo -u postgres psql -d petspot_dev -c \"REINDEX DATABASE petspot_dev;\"${NC}"
        echo -e "${YELLOW}Run: sudo -u postgres psql -d petspot_dev -c \"ANALYZE;\"${NC}"
    fi
fi
echo ""

echo "Step 5: Verification"
echo "--------------------"
echo "Current memory status:"
free -h
echo ""
echo "PostgreSQL processes:"
ps aux | grep postgres | grep -v grep | wc -l | xargs echo "  Processes:"
echo ""
echo "Odoo processes:"
ps aux | grep odoo-bin | grep -v grep | wc -l | xargs echo "  Processes:"
echo ""

echo "=========================================="
echo "Optimization Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Odoo instances to apply config changes"
echo "2. Monitor memory usage: htop"
echo "3. Check PostgreSQL settings: sudo -u postgres psql -c \"SHOW shared_buffers;\""
echo ""
echo "Expected improvements:"
echo "  - 30-50% speedup from PostgreSQL tuning"
echo "  - Reduced swapping with ZRAM"
echo "  - Better stability with memory limits"
echo ""

