"""
Test Script: Check Violation Detection & Database Saving
Run this to debug why violations aren't showing in database
"""

from app.models import CustomUser, RegisteredUser, UserViolation

print("=" * 60)
print("DATABASE STATUS CHECK")
print("=" * 60)

# Check CustomUser table
print("\n1. CUSTOM USERS:")
users = CustomUser.objects.all()
print(f"   Total users: {users.count()}")
for user in users:
    print(f"   - {user.first_name} {user.last_name} | License: {user.license_number} | Phone: {user.phone}")

# Check RegisteredUser table
print("\n2. REGISTERED VEHICLES:")
vehicles = RegisteredUser.objects.all()
print(f"   Total vehicles: {vehicles.count()}")
for vehicle in vehicles:
    print(f"   - Vehicle: {vehicle.vehicle_number} | Phone: {vehicle.phone_number} | Active: {vehicle.is_active}")

# Check UserViolation table
print("\n3. VIOLATIONS IN DATABASE:")
violations = UserViolation.objects.all()
print(f"   Total violations: {violations.count()}")
if violations.count() > 0:
    for v in violations:
        print(f"   - Plate: {v.plate_number} | Type: {v.violation_type} | Severity: {v.severity} | Date: {v.detected_at}")
else:
    print("   ⚠️ NO VIOLATIONS FOUND IN DATABASE!")

# Check specific user's violations
print("\n4. CHECK SPECIFIC USER'S VIOLATIONS:")
test_phone = "8157968294"  # Kailas's phone
try:
    custom_user = CustomUser.objects.get(phone=test_phone)
    print(f"   User: {custom_user.first_name} {custom_user.last_name}")
    
    registered_vehicle = RegisteredUser.objects.filter(phone_number=test_phone).first()
    if registered_vehicle:
        print(f"   Registered Vehicle: {registered_vehicle.vehicle_number}")
        
        user_violations = UserViolation.objects.filter(registered_user=registered_vehicle)
        print(f"   Violations for this user: {user_violations.count()}")
        for v in user_violations:
            print(f"   - {v.violation_type} | {v.plate_number} | {v.detected_at}")
    else:
        print("   ⚠️ No registered vehicle for this user!")
        
except CustomUser.DoesNotExist:
    print(f"   User with phone {test_phone} not found!")

print("\n" + "=" * 60)
print("DIAGNOSIS")
print("=" * 60)

# Diagnosis
if violations.count() == 0:
    print("\n⚠️ ISSUE: No violations in database at all!")
    print("\nPOSSIBLE CAUSES:")
    print("1. Video processing isn't detecting violations")
    print("2. Violations detected but plate numbers don't match registered vehicles")
    print("3. process_video() function has an error")
    print("\nSOLUTION:")
    print("1. Make sure you have registered vehicles in database ✓")
    print("2. Upload a video with those exact plate numbers")
    print("3. Check production_processor.py for detection issues")
elif violations.count() > 0:
    print("\n✓ Violations exist in database")
    print("If dashboard not showing them, check:")
    print("1. User is logged in with correct credentials")
    print("2. User has registered vehicle matching violation plate")
    print("3. Dashboard query is filtering correctly")

print("\n" + "=" * 60)
