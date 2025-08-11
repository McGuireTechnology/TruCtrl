# TruCtrl Management Scripts

This directory contains management scripts for TruCtrl database operations.

## Scripts

### 1. `admin.py` - Admin Management
Create and manage admin users directly against the database.

**Usage:**
```bash
# Create an admin user
python scripts/admin.py create admin@example.com --name "Admin User"

# List all users
python scripts/admin.py list

# List only active users
python scripts/admin.py list --active-only

# Activate a user
python scripts/admin.py activate user@example.com

# Deactivate a user
python scripts/admin.py deactivate user@example.com

# Reset user password
python scripts/admin.py reset-password user@example.com

# Delete a user
python scripts/admin.py delete user@example.com

# Show database information
python scripts/admin.py info
```

### 2. `user_manager.py` - User Management
Comprehensive user management with bulk operations.

**Usage:**
```bash
# Create a user
python scripts/user_manager.py create user@example.com --name "User Name"

# Create an inactive user
python scripts/user_manager.py create user@example.com --name "User Name" --inactive

# Update user information
python scripts/user_manager.py update user@example.com --name "New Name" --new-email newemail@example.com

# Show user information
python scripts/user_manager.py info user@example.com

# Bulk create users from CSV
python scripts/user_manager.py bulk-create users.csv

# Export users to CSV
python scripts/user_manager.py export users.csv --format csv

# Export users to JSON
python scripts/user_manager.py export users.json --format json

# Search users
python scripts/user_manager.py search "john"

# Show user statistics
python scripts/user_manager.py stats
```

### 3. `db_manager.py` - Database Management
Database backup, restore, and maintenance operations.

**Usage:**
```bash
# Create database backup
python scripts/db_manager.py backup

# Create backup with custom path
python scripts/db_manager.py backup --path /path/to/backup.db

# Restore database from backup
python scripts/db_manager.py restore /path/to/backup.db

# Run database migrations
python scripts/db_manager.py migrate

# Create new migration
python scripts/db_manager.py create-migration "Add new feature"

# Show database information
python scripts/db_manager.py info

# Vacuum database (reclaim space)
python scripts/db_manager.py vacuum

# Check database integrity
python scripts/db_manager.py check
```

## CSV Format for Bulk User Creation

The CSV file should have the following columns:
- `email`: User email address (required)
- `name`: User full name (required)
- `password`: User password (required)
- `is_active`: Boolean (true/false, optional, defaults to true)

See `example_users.csv` for a template.

## Security Notes

- All passwords are hashed using bcrypt before storage
- Scripts require direct database access
- Always backup your database before running destructive operations
- Use strong passwords (minimum 8 characters)

## Requirements

Make sure you have the following dependencies installed:
```bash
pip install PyJWT passlib[bcrypt] python-multipart
```

## Environment

Scripts use the same database configuration as the main application (`api/app/config.py`).
