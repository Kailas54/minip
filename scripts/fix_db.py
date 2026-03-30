import os
import django
import sys
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini.settings')
django.setup()

from app.models import CustomUser, RegisteredUser

def norm(p):
    return re.sub(r'[^A-Z0-9]', '', str(p).upper()) if p else ''

for u in CustomUser.objects.all():
    original = u.license_number
    normalized = norm(u.license_number)
    if original != normalized:
        print(f"CustomUser: {original} -> {normalized}")
        try:
            u.license_number = normalized
            u.save()
        except Exception as e:
            print(f"Failed to save CustomUser {u.id}: {e}")

for r in RegisteredUser.objects.all():
    original = r.vehicle_number
    normalized = norm(r.vehicle_number)
    if original != normalized:
        print(f"RegisteredUser: {original} -> {normalized}")
        try:
            r.vehicle_number = normalized
            r.save()
        except Exception as e:
            print(f"Failed to save RegisteredUser {r.id}: {e}")

print("Fixed DB.")
