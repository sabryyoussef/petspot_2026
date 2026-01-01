#!/usr/bin/env python3
"""
Odoo Instance Sync Script
Syncs data from production Odoo instance to development instance
- First run: Full sync
- Subsequent runs: Only new/updated records
"""

import xmlrpc.client
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
CONFIG = {
    'source': {
        'url': 'http://localhost:8069',
        'db': 'petspot',
        'username': 'admin',
        'password': 'admin',  # Using password for authentication
        'api_key': 'f1d91badd68658e938f9e7738d409ff71a139192'  # Backup API key
    },
    'target': {
        'url': 'http://localhost:8070',
        'db': 'petspot_dev',
        'username': 'admin',
        'password': 'admin'
    }
}

# Tracking file for sync state
SYNC_STATE_FILE = '/home/petspot/odoo-19/sync_state.json'

# Models to sync in order (respecting dependencies)
MODELS_TO_SYNC = [
    # Base models first
    'res.country',
    'res.country.state',
    'res.currency',
    'res.lang',
    'res.company',
    'res.users',
    'res.groups',
    'res.partner.title',
    'res.partner.category',
    'res.partner.industry',
    
    # Partners
    'res.partner',
    
    # Product related
    'product.category',
    'uom.category',
    'uom.uom',
    'product.attribute',
    'product.attribute.value',
    'product.template',
    'product.product',
    'product.pricelist',
    'product.pricelist.item',
    
    # Accounting
    'account.account.type',
    'account.account',
    'account.journal',
    'account.tax.group',
    'account.tax',
    'account.fiscal.position',
    'account.payment.term',
    
    # Sales
    'sale.order',
    'sale.order.line',
    
    # Purchase
    'purchase.order',
    'purchase.order.line',
    
    # Inventory
    'stock.location',
    'stock.warehouse',
    'stock.picking.type',
    'stock.picking',
    'stock.move',
    'stock.move.line',
    
    # Invoicing
    'account.move',
    'account.move.line',
    'account.payment',
    
    # CRM
    'crm.team',
    'crm.stage',
    'crm.lead',
    
    # HR (if installed)
    'hr.department',
    'hr.job',
    'hr.employee',
    
    # Project (if installed)
    'project.project',
    'project.task',
]


class OdooSync:
    def __init__(self):
        self.source_common = None
        self.source_models = None
        self.source_uid = None
        self.source_auth = None  # Store the working authentication credential
        
        self.target_common = None
        self.target_models = None
        self.target_uid = None
        self.target_auth = None
        
        self.sync_state = self.load_sync_state()
        self.model_mapping = {}  # Maps source IDs to target IDs
        
    def load_sync_state(self) -> Dict:
        """Load previous sync state"""
        if os.path.exists(SYNC_STATE_FILE):
            with open(SYNC_STATE_FILE, 'r') as f:
                return json.load(f)
        return {
            'last_sync': None,
            'models_synced': {},
            'id_mapping': {}
        }
    
    def save_sync_state(self):
        """Save current sync state"""
        self.sync_state['last_sync'] = datetime.now().isoformat()
        with open(SYNC_STATE_FILE, 'w') as f:
            json.dump(self.sync_state, f, indent=2)
    
    def connect_source(self):
        """Connect to source Odoo instance"""
        print("🔗 Connecting to SOURCE (Production)...")
        url = CONFIG['source']['url']
        db = CONFIG['source']['db']
        username = CONFIG['source']['username']
        password = CONFIG['source'].get('password', 'admin')
        
        self.source_common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.source_models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        try:
            # Test connection by getting version
            version = self.source_common.version()
            print(f"   Source Odoo version: {version.get('server_version', 'unknown')}")
            
            # Authenticate with password
            self.source_uid = self.source_common.authenticate(db, username, password, {})
            self.source_auth = password
            
            if not self.source_uid:
                raise Exception("Failed to authenticate with source Odoo instance")
                
        except Exception as e:
            print(f"   Error: {e}")
            raise Exception(f"Failed to connect to source Odoo instance: {e}")
        
        print(f"✅ Connected to SOURCE - User ID: {self.source_uid}")
        return self.source_uid
    
    def connect_target(self):
        """Connect to target Odoo instance"""
        print("🔗 Connecting to TARGET (Development)...")
        url = CONFIG['target']['url']
        db = CONFIG['target']['db']
        username = CONFIG['target']['username']
        password = CONFIG['target']['password']
        
        self.target_common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.target_models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
        try:
            # Test connection
            version = self.target_common.version()
            print(f"   Target Odoo version: {version.get('server_version', 'unknown')}")
            
            # Authenticate with password
            self.target_uid = self.target_common.authenticate(db, username, password, {})
            self.target_auth = password
            
            if not self.target_uid:
                raise Exception("Failed to authenticate with target Odoo instance")
                
        except Exception as e:
            print(f"   Error: {e}")
            raise Exception(f"Failed to connect to target Odoo instance: {e}")
        
        print(f"✅ Connected to TARGET - User ID: {self.target_uid}")
        return self.target_uid
    
    def get_model_fields(self, model_name: str, is_source: bool = True) -> Dict:
        """Get fields for a model"""
        models = self.source_models if is_source else self.target_models
        uid = self.source_uid if is_source else self.target_uid
        db = CONFIG['source']['db'] if is_source else CONFIG['target']['db']
        auth = self.source_auth if is_source else self.target_auth
        
        try:
            fields = models.execute_kw(
                db, uid, auth,
                model_name, 'fields_get',
                [],
                {'attributes': ['type', 'relation', 'required', 'readonly']}
            )
            return fields
        except Exception as e:
            print(f"⚠️  Could not get fields for {model_name}: {e}")
            return {}
    
    def search_records(self, model_name: str, domain: List = None, is_source: bool = True) -> List[int]:
        """Search for records in a model"""
        models = self.source_models if is_source else self.target_models
        uid = self.source_uid if is_source else self.target_uid
        db = CONFIG['source']['db'] if is_source else CONFIG['target']['db']
        auth = self.source_auth if is_source else self.target_auth
        
        if domain is None:
            domain = []
        
        try:
            record_ids = models.execute_kw(
                db, uid, auth,
                model_name, 'search',
                [domain]
            )
            return record_ids
        except Exception as e:
            print(f"⚠️  Could not search {model_name}: {e}")
            return []
    
    def read_records(self, model_name: str, record_ids: List[int], fields: List[str] = None) -> List[Dict]:
        """Read records from source"""
        if not record_ids:
            return []
        
        try:
            records = self.source_models.execute_kw(
                CONFIG['source']['db'],
                self.source_uid,
                self.source_auth,
                model_name, 'read',
                [record_ids],
                {'fields': fields} if fields else {}
            )
            return records
        except Exception as e:
            print(f"⚠️  Could not read {model_name}: {e}")
            return []
    
    def prepare_record_data(self, model_name: str, record: Dict, fields: Dict) -> Optional[Dict]:
        """Prepare record data for creation in target"""
        data = {}
        
        # Skip id and internal fields
        skip_fields = ['id', '__last_update', 'display_name', 'create_date', 
                       'create_uid', 'write_date', 'write_uid', 'message_ids',
                       'activity_ids', 'message_follower_ids', 'website_message_ids']
        
        for field_name, field_value in record.items():
            if field_name in skip_fields:
                continue
            
            if field_name not in fields:
                continue
            
            field_info = fields[field_name]
            field_type = field_info.get('type')
            
            # Handle readonly and computed fields
            if field_info.get('readonly') and not field_info.get('required'):
                continue
            
            # Handle different field types
            if field_type == 'many2one':
                if field_value:
                    # field_value is [id, name] tuple
                    source_id = field_value[0] if isinstance(field_value, list) else field_value
                    relation_model = field_info.get('relation')
                    
                    # Try to map to target ID
                    mapping_key = f"{relation_model}_{source_id}"
                    if mapping_key in self.sync_state.get('id_mapping', {}):
                        data[field_name] = self.sync_state['id_mapping'][mapping_key]
                    else:
                        # Try to find by name or external_id
                        data[field_name] = False  # Skip for now
                else:
                    data[field_name] = False
            
            elif field_type in ['one2many', 'many2many']:
                # Skip for initial creation, handle separately
                continue
            
            elif field_type == 'binary':
                # Handle binary fields (images, attachments)
                data[field_name] = field_value if field_value else False
            
            else:
                # Simple field types: char, text, integer, float, boolean, date, datetime, selection
                data[field_name] = field_value if field_value is not False else False
        
        return data if data else None
    
    def create_record(self, model_name: str, data: Dict) -> Optional[int]:
        """Create record in target"""
        try:
            record_id = self.target_models.execute_kw(
                CONFIG['target']['db'],
                self.target_uid,
                self.target_auth,
                model_name, 'create',
                [data]
            )
            return record_id
        except Exception as e:
            print(f"❌ Error creating record in {model_name}: {e}")
            print(f"   Data: {data}")
            return None
    
    def sync_model(self, model_name: str, incremental: bool = False):
        """Sync a specific model"""
        print(f"\n📦 Syncing model: {model_name}")
        
        # Check if model exists in both instances
        try:
            source_fields = self.get_model_fields(model_name, is_source=True)
            target_fields = self.get_model_fields(model_name, is_source=False)
            
            if not source_fields or not target_fields:
                print(f"⚠️  Skipping {model_name} - model not available in both instances")
                return
        except Exception as e:
            print(f"⚠️  Skipping {model_name}: {e}")
            return
        
        # Build search domain for incremental sync
        domain = []
        if incremental and model_name in self.sync_state.get('models_synced', {}):
            last_sync = self.sync_state['models_synced'][model_name].get('last_sync')
            if last_sync:
                domain = ['|', ('create_date', '>', last_sync), ('write_date', '>', last_sync)]
        
        # Search for records in source
        record_ids = self.search_records(model_name, domain, is_source=True)
        
        if not record_ids:
            print(f"✅ No records to sync for {model_name}")
            return
        
        print(f"📊 Found {len(record_ids)} records to sync")
        
        # Read records from source
        records = self.read_records(model_name, record_ids)
        
        synced_count = 0
        failed_count = 0
        
        for record in records:
            source_id = record['id']
            
            # Prepare data for target
            data = self.prepare_record_data(model_name, record, source_fields)
            
            if not data:
                continue
            
            # Create in target
            target_id = self.create_record(model_name, data)
            
            if target_id:
                # Store ID mapping
                mapping_key = f"{model_name}_{source_id}"
                if 'id_mapping' not in self.sync_state:
                    self.sync_state['id_mapping'] = {}
                self.sync_state['id_mapping'][mapping_key] = target_id
                synced_count += 1
            else:
                failed_count += 1
        
        # Update sync state for this model
        if 'models_synced' not in self.sync_state:
            self.sync_state['models_synced'] = {}
        
        self.sync_state['models_synced'][model_name] = {
            'last_sync': datetime.now().isoformat(),
            'records_synced': synced_count,
            'records_failed': failed_count
        }
        
        print(f"✅ Synced: {synced_count} | ❌ Failed: {failed_count}")
    
    def sync_all(self, incremental: bool = False):
        """Sync all models"""
        print("\n" + "="*60)
        print("🚀 ODOO INSTANCE SYNC")
        print("="*60)
        print(f"Mode: {'INCREMENTAL' if incremental else 'FULL SYNC'}")
        print(f"Source: {CONFIG['source']['db']} @ {CONFIG['source']['url']}")
        print(f"Target: {CONFIG['target']['db']} @ {CONFIG['target']['url']}")
        print("="*60)
        
        # Connect to both instances
        self.connect_source()
        self.connect_target()
        
        # Sync each model
        for model_name in MODELS_TO_SYNC:
            try:
                self.sync_model(model_name, incremental=incremental)
            except Exception as e:
                print(f"❌ Error syncing {model_name}: {e}")
                continue
        
        # Save sync state
        self.save_sync_state()
        
        print("\n" + "="*60)
        print("✅ SYNC COMPLETED!")
        print("="*60)
        print(f"State saved to: {SYNC_STATE_FILE}")


def main():
    """Main entry point"""
    syncer = OdooSync()
    
    # Check if this is first run
    is_first_run = syncer.sync_state.get('last_sync') is None
    
    if is_first_run:
        print("\n🆕 First run detected - performing FULL SYNC")
        syncer.sync_all(incremental=False)
    else:
        print("\n♻️  Previous sync found - performing INCREMENTAL SYNC")
        print(f"Last sync: {syncer.sync_state.get('last_sync')}")
        syncer.sync_all(incremental=True)


if __name__ == '__main__':
    main()

