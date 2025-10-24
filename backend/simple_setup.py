#!/usr/bin/env python3
"""
Simple database setup script for inventory management system.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent))

def main():
    print("🚀 Simple Database Setup")
    print("=" * 50)
    
    print("\n1. First, make sure you've updated your .env file with:")
    print("   - SUPABASE_URL (from your Supabase project)")
    print("   - SUPABASE_SERVICE_KEY (service role key)")
    print("   - JWT_SECRET_KEY (32+ character random string)")
    
    print("\n2. Go to your Supabase Dashboard > SQL Editor")
    
    print("\n3. Copy and paste this SQL to create tables:")
    print("-" * 30)
    
    # Read and display the migration SQL
    sql_file = Path(__file__).parent / "migrations" / "001_create_tables.sql"
    if sql_file.exists():
        with open(sql_file, 'r') as f:
            print(f.read())
    else:
        print("Migration file not found!")
        return
    
    print("\n4. Then run this SQL to create the admin user:")
    print("-" * 30)
    
    # Read and display the seed SQL
    seed_file = Path(__file__).parent / "migrations" / "002_seed_data.sql"
    if seed_file.exists():
        with open(seed_file, 'r') as f:
            print(f.read())
    else:
        print("Seed file not found!")
        return
    
    print("\n5. Default admin credentials:")
    print("   Email: admin@admin.com")
    print("   Password: admin123!")
    
    print("\n✅ Setup complete! You can now test your API.")

if __name__ == "__main__":
    main()