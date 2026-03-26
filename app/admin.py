from django.contrib import admin
from .models import CustomUser  # Import your User model
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'first_name', 'last_name', 'address', 'phone', 'age')

