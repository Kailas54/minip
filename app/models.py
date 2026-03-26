from django.db import models

class CustomUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    age = models.PositiveIntegerField()

    class Meta:
        db_table = 'CustomUser'
    
    def __str__(self):
        return f"{self.license_number} - {self.phone}"


class RegisteredUser(models.Model):
    """Store user phone numbers and vehicle details for alerts"""
    phone_number = models.CharField(max_length=15, unique=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.phone_number}"


class UserViolation(models.Model):
    """Store violations linked to registered users"""
    registered_user = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='violations')
    violation_type = models.CharField(max_length=50)  # overspeeding, no_helmet
    speed = models.CharField(max_length=20, blank=True, null=True)
    plate_number = models.CharField(max_length=20)
    frame_time = models.CharField(max_length=20)
    severity = models.CharField(max_length=20)
    detected_at = models.DateTimeField(auto_now_add=True)
    video_file = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.plate_number} - {self.violation_type}"
