#!/usr/bin/env python3
"""
Admin management script for TruCtrl
Usage: python scripts/admin.py [command] [options]
"""

import argparse
import sys
import os
from pathlib import Path

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

def create_admin_user(email: str, password: str, name: str = None):
    """Create a new admin user"""
    try:
        with Session(engine) as db:
            # Check if user already exists
            existing_user = get_user_by_email(db, email)
            if existing_user:
                print(f"❌ User with email {email} already exists!")
                return False
            
            # Create new admin user
            hashed_password = get_password_hash(password)
            admin_user = User(
                email=email,
                name=name or email.split('@')[0],
                password=hashed_password,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            print(f"✅ Admin user created successfully!")
            print(f"   Email: {email}")
            print(f"   Name: {admin_user.name}")
            print(f"   ID: {admin_user.id}")
            return True
            
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        return False

def list_users(active_only: bool = False):
    """List all users"""
    try:
        with Session(engine) as db:
            statement = select(User)
            if active_only:
                statement = statement.where(User.is_active == True)
            
            users = db.exec(statement).all()
            
            if not users:
                print("No users found.")
                return
            
            title = "📋 Users" + (" (Active only)" if active_only else "")
            print(f"\n{title}:")
            print("-" * 80)
            print(f"{'ID':<30} {'Email':<30} {'Name':<20} {'Active':<8}")
            print("-" * 80)
            
            for user in users:
                active_status = "✅ Yes" if user.is_active else "❌ No"
                print(f"{user.id:<30} {user.email:<30} {user.name:<20} {active_status:<8}")
            
            print("-" * 80)
            print(f"Total: {len(users)} users")
            
    except Exception as e:
        print(f"❌ Error listing users: {str(e)}")

def activate_user(email: str):
    """Activate a user"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            if user.is_active:
                print(f"❌ User {email} is already active!")
                return False
            
            user.is_active = True
            db.add(user)
            db.commit()
            
            print(f"✅ User {email} activated successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error activating user: {str(e)}")
        return False

def deactivate_user(email: str):
    """Deactivate a user"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            if not user.is_active:
                print(f"❌ User {email} is already deactivated!")
                return False
            
            user.is_active = False
            db.add(user)
            db.commit()
            
            print(f"✅ User {email} deactivated successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error deactivating user: {str(e)}")
        return False

def reset_password(email: str):
    """Reset user password"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            # Get new password
            while True:
                password = getpass.getpass("Enter new password: ")
                confirm_password = getpass.getpass("Confirm new password: ")
                
                if password != confirm_password:
                    print("❌ Passwords don't match! Please try again.")
                    continue
                
                if len(password) < 8:
                    print("❌ Password must be at least 8 characters long!")
                    continue
                
                break
            
            user.password = get_password_hash(password)
            db.add(user)
            db.commit()
            
            print(f"✅ Password reset successfully for {email}")
            return True
            
    except Exception as e:
        print(f"❌ Error resetting password: {str(e)}")
        return False

def delete_user(email: str):
    """Delete a user"""
    try:
        with Session(engine) as db:
            user = get_user_by_email(db, email)
            if not user:
                print(f"❌ User with email {email} not found!")
                return False
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete user {email}? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Deletion cancelled.")
                return False
            
            db.delete(user)
            db.commit()
            
            print(f"✅ User {email} deleted successfully")
            return True
            
    except Exception as e:
        print(f"❌ Error deleting user: {str(e)}")
        return False

def database_info():
    """Show database information"""
    try:
        with Session(engine) as db:
            # Count users
            total_users = len(db.exec(select(User)).all())
            active_users = len(db.exec(select(User).where(User.is_active == True)).all())
            
            print("\n📊 Database Information:")
            print("-" * 40)
            print(f"Total Users: {total_users}")
            print(f"Active Users: {active_users}")
            print(f"Inactive Users: {total_users - active_users}")
            print("-" * 40)
            
            # Show recent users
            recent_users = db.exec(select(User).limit(5)).all()
            if recent_users:
                print("\n🕐 Recent Users:")
                for user in recent_users:
                    status = "Active" if user.is_active else "Inactive"
                    print(f"  {user.email} ({status})")
            
    except Exception as e:
        print(f"❌ Error getting database info: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='TruCtrl Admin Management')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create admin command
    create_parser = subparsers.add_parser('create', help='Create admin user')
    create_parser.add_argument('email', help='Admin email address')
    create_parser.add_argument('--name', help='Admin name (optional)')
    
    # List users command
    list_parser = subparsers.add_parser('list', help='List all users')
    list_parser.add_argument('--active-only', action='store_true', help='Show only active users')
    
    # Activate user command
    activate_parser = subparsers.add_parser('activate', help='Activate user')
    activate_parser.add_argument('email', help='User email address')
    
    # Deactivate user command
    deactivate_parser = subparsers.add_parser('deactivate', help='Deactivate user')
    deactivate_parser.add_argument('email', help='User email address')
    
    # Reset password command
    reset_parser = subparsers.add_parser('reset-password', help='Reset user password')
    reset_parser.add_argument('email', help='User email address')
    
    # Delete user command
    delete_parser = subparsers.add_parser('delete', help='Delete user')
    delete_parser.add_argument('email', help='User email address')
    
    # Database info command
    info_parser = subparsers.add_parser('info', help='Show database information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'create':
            # Get password securely
            password = getpass.getpass("Enter admin password: ")
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long!")
                return
            
            create_admin_user(args.email, password, args.name)
            
        elif args.command == 'list':
            list_users(args.active_only)
            
        elif args.command == 'activate':
            activate_user(args.email)
            
        elif args.command == 'deactivate':
            deactivate_user(args.email)
            
        elif args.command == 'reset-password':
            reset_password(args.email)
            
        elif args.command == 'delete':
            delete_user(args.email)
            
        elif args.command == 'info':
            database_info()
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
