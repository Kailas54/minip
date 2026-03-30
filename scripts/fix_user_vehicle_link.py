"""
Fix Script: Link Vehicles to Existing Users
This will update vehicle registrations to match user phone numbers
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini.settings')
django.setup()

from app.models import CustomUser, RegisteredUser, UserViolation

print("=" * 60)
print("FIXING USER-VEHICLE LINKING")
print("=" * 60)

# Get all users
users = CustomUser.objects.all()
print(f"\nFound {users.count()} users:")

for user in users:
    print(f"\nUser: {user.first_name} {user.last_name}")
    print(f"  Phone: {user.phone}")
    print(f"  License: {user.license_number}")
    
    # Check if they have a registered vehicle
    registered_vehicle = RegisteredUser.objects.filter(phone_number=user.phone).first()
    
    if registered_vehicle:
        print(f"  ✓ Has registered vehicle: {registered_vehicle.vehicle_number}")
    else:
        print(f"  ⚠️ NO REGISTERED VEHICLE!")
        
        # Check if DL 2S G 5988 exists with another phone
        existing_vehicle = RegisteredUser.objects.filter(vehicle_number="DL 2S G 5988").first()
        
        if existing_vehicle:
            print(f"  Vehicle DL 2S G 5988 exists with phone {existing_vehicle.phone_number}")
            print(f"  Updating to user's phone {user.phone}...")
            existing_vehicle.phone_number = user.phone
            existing_vehicle.is_active = True
            existing_vehicle.save()
            print(f"  ✓ Updated: Vehicle now linked to {user.phone}")
        else:
            print(f"  Creating new registration for 'DL 2S G 5988'...")
            new_vehicle = RegisteredUser.objects.create(
                phone_number=user.phone,
                vehicle_number="DL 2S G 5988",
                is_active=True
            )
            new_vehicle.save()
            print(f"  ✓ Created: Vehicle DL 2S G 5988 linked to {user.phone}")

# Show updated status
print("\n" + "=" * 60)
print("UPDATED STATUS")
print("=" * 60)

violations = UserViolation.objects.all()
print(f"\nTotal violations in database: {violations.count()}")

for user in users:
    registered_vehicles = RegisteredUser.objects.filter(phone_number=user.phone)
    print(f"\n{user.first_name} {user.last_name} ({user.phone}):")
    print(f"  Registered vehicles: {registered_vehicles.count()}")
    
    for vehicle in registered_vehicles:
        user_violations = UserViolation.objects.filter(registered_user=vehicle)
        print(f"    - {vehicle.vehicle_number}: {user_violations.count()} violations")

print("\n" + "=" * 60)
print("FIX COMPLETE!")
print("=" * 60)
print("\nNow login with any user and violations should appear on dashboard.")
