#!/usr/bin/env python3
"""
Database management script for TruCtrl
Usage: python scripts/db_manager.py [command] [options]
"""

import argparse
import sys
import os
from pathlib import Path
import sqlite3
import json
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.app.db import engine
from api.app.models import User
from api.app.config import settings
from sqlmodel import Session, select, text
import subprocess

def backup_database(backup_path: str = None):
    """Create a backup of the database"""
    try:
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_tructrl_{timestamp}.db"
        
        # For SQLite, we can use the backup API
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return False
        
        # Create backup
        source = sqlite3.connect(db_path)
        backup = sqlite3.connect(backup_path)
        
        source.backup(backup)
        
        source.close()
        backup.close()
        
        print(f"✅ Database backup created: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        return False

def restore_database(backup_path: str):
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_path):
            print(f"❌ Backup file not found: {backup_path}")
            return False
        
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        
        # Confirm restoration
        confirm = input(f"Are you sure you want to restore from {backup_path}? This will overwrite the current database. (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ Restoration cancelled.")
            return False
        
        # Create backup of current database first
        current_backup = f"pre_restore_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        if os.path.exists(db_path):
            backup_database(current_backup)
            print(f"📁 Current database backed up to: {current_backup}")
        
        # Restore from backup
        source = sqlite3.connect(backup_path)
        target = sqlite3.connect(db_path)
        
        source.backup(target)
        
        source.close()
        target.close()
        
        print(f"✅ Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error restoring database: {str(e)}")
        return False

def run_migration():
    """Run database migrations"""
    try:
        print("🔄 Running database migrations...")
        
        # Run alembic upgrade
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migrations completed successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Migration failed!")
            if result.stderr:
                print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running migrations: {str(e)}")
        return False

def create_migration(message: str):
    """Create a new migration"""
    try:
        print(f"📝 Creating migration: {message}")
        
        # Run alembic revision
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", message],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Migration created successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Migration creation failed!")
            if result.stderr:
                print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error creating migration: {str(e)}")
        return False

def database_info():
    """Show database information"""
    try:
        with Session(engine) as db:
            # Get database file info
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            
            if os.path.exists(db_path):
                file_size = os.path.getsize(db_path)
                file_size_mb = file_size / (1024 * 1024)
                modified_time = datetime.fromtimestamp(os.path.getmtime(db_path))
            else:
                file_size_mb = 0
                modified_time = "N/A"
            
            # Get table information
            tables_info = db.exec(text("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)).all()
            
            print("\n📊 Database Information:")
            print("-" * 50)
            print(f"Database Path: {db_path}")
            print(f"File Size: {file_size_mb:.2f} MB")
            print(f"Last Modified: {modified_time}")
            print(f"Tables: {len(tables_info)}")
            print("-" * 50)
            
            # Show tables
            print("\n📋 Tables:")
            for table in tables_info:
                # Get row count
                try:
                    count_result = db.exec(text(f"SELECT COUNT(*) FROM {table.name}")).first()
                    row_count = count_result[0] if count_result else 0
                    print(f"  {table.name}: {row_count} rows")
                except:
                    print(f"  {table.name}: Unable to count rows")
            
            return True
            
    except Exception as e:
        print(f"❌ Error getting database info: {str(e)}")
        return False

def vacuum_database():
    """Vacuum the database to reclaim space"""
    try:
        print("🧹 Vacuuming database...")
        
        with Session(engine) as db:
            db.exec(text("VACUUM"))
            db.commit()
        
        print("✅ Database vacuumed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error vacuuming database: {str(e)}")
        return False

def check_database_integrity():
    """Check database integrity"""
    try:
        print("🔍 Checking database integrity...")
        
        with Session(engine) as db:
            result = db.exec(text("PRAGMA integrity_check")).first()
            
            if result and result[0] == "ok":
                print("✅ Database integrity check passed!")
                return True
            else:
                print(f"❌ Database integrity check failed: {result}")
                return False
        
    except Exception as e:
        print(f"❌ Error checking database integrity: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='TruCtrl Database Management')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create database backup')
    backup_parser.add_argument('--path', help='Backup file path (optional)')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore database from backup')
    restore_parser.add_argument('backup_path', help='Backup file path')
    
    # Migration commands
    migrate_parser = subparsers.add_parser('migrate', help='Run database migrations')
    
    create_migration_parser = subparsers.add_parser('create-migration', help='Create new migration')
    create_migration_parser.add_argument('message', help='Migration message')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show database information')
    
    # Vacuum command
    vacuum_parser = subparsers.add_parser('vacuum', help='Vacuum database')
    
    # Integrity check command
    integrity_parser = subparsers.add_parser('check', help='Check database integrity')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'backup':
            backup_database(args.path)
            
        elif args.command == 'restore':
            restore_database(args.backup_path)
            
        elif args.command == 'migrate':
            run_migration()
            
        elif args.command == 'create-migration':
            create_migration(args.message)
            
        elif args.command == 'info':
            database_info()
            
        elif args.command == 'vacuum':
            vacuum_database()
            
        elif args.command == 'check':
            check_database_integrity()
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
