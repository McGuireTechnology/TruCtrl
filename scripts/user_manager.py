#!/usr/bin/env python3
"""
User management script for TruCtrl
Usage: python scripts/user_manager.py [command] [options]
"""

import argparse
import sys
import os
from pathlib import Path
import csv
import json
from typing import List, Dict

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.app.db import engine
from api.app.models import User
from api.app.security import get_password_hash, verify_password
from api.app.crud import get_user_by_email
from sqlmodel import Session, select
from datetime import datetime
import getpass

def create_user(email: str, password: str, name: str = None, is_active: bool = True):
    """Create a new user"""
    try:
        with Session(engine) as db:
            # Check if user already exists
            existing_user = get_user_by_email(db, email)
            if existing_user:
                print(f"❌ User with email {email} already exists!")
                return False
            
            # Create new user
            hashed_password = get_password_hash(password)
            user = User(
                email=email,
                name=name or email.split('@')[0],
                password=hashed_password,
                is_active=is_active
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            print(f"✅ User created successfully!")
            print(f"   Email: {email}")
            print(f"   Name: {user.name}")
            print(f"   ID: {user.id}")
            print(f"   Active: {user.is_active}")
            return True
            
    except Exception as e:
        print(f"❌ Error creating user: {str(e)}")
        return False

def update_user(email: str, name: str = None, new_email: str = None):
    """Update user information"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            # Update fields
            if name:
                user.name = name
            if new_email:
                # Check if new email is already taken
                existing = get_user_by_email(db, new_email)
                if existing and existing.id != user.id:
                    print(f"❌ Email {new_email} is already taken!")
                    return False
                user.email = new_email
            
            db.add(user)
            db.commit()
            
            print(f"✅ User updated successfully!")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.name}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating user: {str(e)}")
        return False

def user_info(email: str):
    """Show detailed user information"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            print(f"\n👤 User Information:")
            print("-" * 40)
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Name: {user.name}")
            print(f"Active: {'✅ Yes' if user.is_active else '❌ No'}")
            print("-" * 40)
            return True
            
    except Exception as e:
        print(f"❌ Error getting user info: {str(e)}")
        return False

def bulk_create_users(csv_file: str):
    """Create users from CSV file"""
    try:
        if not os.path.exists(csv_file):
            print(f"❌ CSV file {csv_file} not found!")
            return False
        
        created_count = 0
        failed_count = 0
        
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            
            # Validate headers
            required_headers = ['email', 'name', 'password']
            if not all(header in reader.fieldnames for header in required_headers):
                print(f"❌ CSV file must have headers: {', '.join(required_headers)}")
                print(f"   Found headers: {', '.join(reader.fieldnames)}")
                return False
            
            for row in reader:
                email = row['email'].strip()
                name = row['name'].strip()
                password = row['password'].strip()
                is_active = row.get('is_active', 'true').lower() == 'true'
                
                if not email or not name or not password:
                    print(f"❌ Skipping row with missing data: {row}")
                    failed_count += 1
                    continue
                
                if create_user(email, password, name, is_active):
                    created_count += 1
                else:
                    failed_count += 1
        
        print(f"\n📊 Bulk creation summary:")
        print(f"   Created: {created_count}")
        print(f"   Failed: {failed_count}")
        return True
        
    except Exception as e:
        print(f"❌ Error in bulk creation: {str(e)}")
        return False

def export_users(output_file: str, format: str = 'csv'):
    """Export users to CSV or JSON"""
    try:
        with Session(engine) as db:
            users = db.exec(select(User)).all()
            
            if format.lower() == 'csv':
                with open(output_file, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['id', 'email', 'name', 'is_active'])
                    
                    for user in users:
                        writer.writerow([user.id, user.email, user.name, user.is_active])
                        
            elif format.lower() == 'json':
                user_data = []
                for user in users:
                    user_data.append({
                        'id': user.id,
                        'email': user.email,
                        'name': user.name,
                        'is_active': user.is_active
                    })
                
                with open(output_file, 'w') as file:
                    json.dump(user_data, file, indent=2)
            
            else:
                print(f"❌ Unsupported format: {format}")
                return False
            
            print(f"✅ Exported {len(users)} users to {output_file}")
            return True
            
    except Exception as e:
        print(f"❌ Error exporting users: {str(e)}")
        return False

def search_users(query: str):
    """Search users by email or name"""
    try:
        with Session(engine) as db:
            statement = select(User).where(
                (User.email.contains(query)) | (User.name.contains(query))
            )
            users = db.exec(statement).all()
            
            if not users:
                print(f"No users found matching: {query}")
                return
            
            print(f"\n🔍 Search results for '{query}':")
            print("-" * 80)
            print(f"{'ID':<30} {'Email':<30} {'Name':<20} {'Active':<8}")
            print("-" * 80)
            
            for user in users:
                active_status = "✅ Yes" if user.is_active else "❌ No"
                print(f"{user.id:<30} {user.email:<30} {user.name:<20} {active_status:<8}")
            
            print("-" * 80)
            print(f"Found: {len(users)} users")
            
    except Exception as e:
        print(f"❌ Error searching users: {str(e)}")

def user_stats():
    """Show user statistics"""
    try:
        with Session(engine) as db:
            total_users = len(db.exec(select(User)).all())
            active_users = len(db.exec(select(User).where(User.is_active == True)).all())
            inactive_users = total_users - active_users
            
            print("\n📊 User Statistics:")
            print("-" * 30)
            print(f"Total Users: {total_users}")
            print(f"Active Users: {active_users}")
            print(f"Inactive Users: {inactive_users}")
            print(f"Activation Rate: {(active_users/total_users*100):.1f}%" if total_users > 0 else "N/A")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error getting user stats: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='TruCtrl User Management')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create user command
    create_parser = subparsers.add_parser('create', help='Create user')
    create_parser.add_argument('email', help='User email address')
    create_parser.add_argument('--name', help='User name (optional)')
    create_parser.add_argument('--inactive', action='store_true', help='Create inactive user')
    
    # Update user command
    update_parser = subparsers.add_parser('update', help='Update user')
    update_parser.add_argument('email', help='Current user email')
    update_parser.add_argument('--name', help='New name')
    update_parser.add_argument('--new-email', help='New email address')
    
    # User info command
    info_parser = subparsers.add_parser('info', help='Show user information')
    info_parser.add_argument('email', help='User email address')
    
    # Bulk create command
    bulk_parser = subparsers.add_parser('bulk-create', help='Create users from CSV')
    bulk_parser.add_argument('csv_file', help='Path to CSV file')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export users')
    export_parser.add_argument('output_file', help='Output file path')
    export_parser.add_argument('--format', choices=['csv', 'json'], default='csv', help='Export format')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search users')
    search_parser.add_argument('query', help='Search query (email or name)')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show user statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'create':
            # Get password securely
            password = getpass.getpass("Enter user password: ")
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long!")
                return
            
            is_active = not args.inactive
            create_user(args.email, password, args.name, is_active)
            
        elif args.command == 'update':
            update_user(args.email, args.name, args.new_email)
            
        elif args.command == 'info':
            user_info(args.email)
            
        elif args.command == 'bulk-create':
            bulk_create_users(args.csv_file)
            
        elif args.command == 'export':
            export_users(args.output_file, args.format)
            
        elif args.command == 'search':
            search_users(args.query)
            
        elif args.command == 'stats':
            user_stats()
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
