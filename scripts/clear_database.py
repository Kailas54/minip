"""
Database Cleanup Script - Delete All Entries
This will remove ALL data from the database (users, vehicles, violations)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini.settings')
django.setup()

from app.models import CustomUser, RegisteredUser, UserViolation

print("=" * 60)
print("⚠️  WARNING: DATABASE CLEANUP ⚠️")
print("=" * 60)
print("\nThis will DELETE ALL data:")
print("  - All user accounts")
print("  - All vehicle registrations")
print("  - All violation records")
print("\nThis action CANNOT be undone!")
print("=" * 60)

# Get current counts
user_count = CustomUser.objects.count()
vehicle_count = RegisteredUser.objects.count()
violation_count = UserViolation.objects.count()

print(f"\nCurrent database contents:")
print(f"  Users: {user_count}")
print(f"  Vehicles: {vehicle_count}")
print(f"  Violations: {violation_count}")
print("=" * 60)

# Confirm deletion
response = input("\nAre you sure you want to delete ALL data? (yes/no): ")

if response.lower() in ['yes', 'y']:
    print("\n🗑️  Deleting all data...")
    
    # Delete all violations
    deleted_violations, _ = UserViolation.objects.all().delete()
    print(f"   ✓ Deleted {deleted_violations} violations")
    
    # Delete all vehicle registrations
    deleted_vehicles, _ = RegisteredUser.objects.all().delete()
    print(f"   ✓ Deleted {deleted_vehicles} vehicle registrations")
    
    # Delete all users
    deleted_users, _ = CustomUser.objects.all().delete()
    print(f"   ✓ Deleted {deleted_users} users")
    
    print("\n" + "=" * 60)
    print("✅ DATABASE CLEANED SUCCESSFULLY!")
    print("=" * 60)
    print("\nDatabase is now empty.")
    print("You can now register new users and test fresh data.")
    
else:
    print("\n❌ Deletion cancelled. No data was deleted.")

print("=" * 60)
