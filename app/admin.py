from django.contrib import admin
from .models import CustomUser, RegisteredUser, UserViolation

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'first_name', 'last_name', 'address', 'phone', 'age')
    search_fields = ['license_number', 'phone', 'first_name', 'last_name']
    list_filter = ['age']

@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'phone_number', 'created_at', 'is_active')
    search_fields = ['vehicle_number', 'phone_number']
    list_filter = ['is_active', 'created_at']

@admin.register(UserViolation)
class UserViolationAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'violation_type', 'speed', 'severity', 'detected_at', 'registered_user')
    search_fields = ['plate_number', 'violation_type']
    list_filter = ['violation_type', 'severity', 'detected_at']

