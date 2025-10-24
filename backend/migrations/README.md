# Database Migrations

This directory contains database migration scripts and utilities for the inventory management system.

## Files

- `001_create_tables.sql` - Creates the initial database schema (users, inventory_items, orders, order_items)
- `002_seed_data.sql` - Seeds the database with default admin user (SQL version)
- `seed_database.py` - Python script for database seeding with bcrypt password hashing
- `run_migrations.py` - Migration runner that executes all migrations and seeding
- `README.md` - This documentation file

## Usage

### Running All Migrations and Seeding

```bash
cd backend/migrations
python run_migrations.py
```

### Running Individual Scripts

#### Create Database Schema
Execute the SQL migration directly in your Supabase SQL editor:
```sql
-- Copy and paste content from 001_create_tables.sql
```

#### Seed Database with Python Script
```bash
cd backend/migrations
python seed_database.py
```

## Default Admin User

After running the seeding script, a default admin user will be created:

- **Email**: admin@admin.com
- **Password**: admin123!
- **Role**: admin
- **Status**: active

**Important**: Change the default admin password after first login in production environments.

## Requirements

Before running migrations, ensure:

1. Supabase project is set up and accessible
2. Environment variables are configured in `.env` file:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `JWT_SECRET_KEY`
3. Python dependencies are installed: `pip install -r requirements.txt`

## Database Schema

The migration creates the following tables:

### users
- User accounts with role-based access control
- Roles: admin, salesperson, warehouse_manager
- Status: invited, active

### inventory_items
- Product inventory with stock tracking
- Includes low stock threshold alerts

### orders
- Customer orders with status tracking
- Status: pending, processing, fulfilled

### order_items
- Individual items within orders
- Links orders to inventory items with quantities

## Indexes

The migration creates indexes for optimal query performance:
- User email, role, and status
- Inventory item names and stock levels
- Order status, creator, and creation date
- Order item relationships

## Triggers

Automatic `updated_at` timestamp triggers are created for:
- users
- inventory_items  
- orders