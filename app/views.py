from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser, RegisteredUser, UserViolation
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import re

def normalize_plate(plate):
    if not plate: return ''
    return re.sub(r'[^A-Z0-9]', '', str(plate).upper())


def home(request):
    return redirect('login')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        license_number = normalize_plate(request.POST.get('license_number'))
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        age = request.POST.get('age')
        
        # Check if license number already exists
        if CustomUser.objects.filter(license_number=license_number).exists():
            return render(request, 'app/register.html', {'error': 'License number already registered'})
        
        # Check if phone number already exists
        if CustomUser.objects.filter(phone=phone).exists():
            return render(request, 'app/register.html', {'error': 'Phone number already registered'})
        
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            phone=phone,
            address=address,
            age=age
        )
        user.save()
        
        # Automatically register the vehicle to enable immediate alerts
        RegisteredUser.objects.get_or_create(
            phone_number=phone,
            defaults={'vehicle_number': license_number}
        )
        
        return redirect('login')
    return render(request, 'app/register.html')


def user_login(request):
    """User login page"""
    if request.method == 'POST':
        license_number = normalize_plate(request.POST.get('license_number'))
        phone = request.POST.get('phone')
        
        try:
            user = CustomUser.objects.get(license_number=license_number, phone=phone)
            request.session['user_license'] = license_number
            request.session['user_phone'] = phone
            request.session['user_name'] = f"{user.first_name} {user.last_name}"
            return redirect('user_dashboard')
        except CustomUser.DoesNotExist:
            return render(request, 'app/login.html', {'error': 'Invalid license number or phone number'})
    
    return render(request, 'app/login.html')


def user_logout(request):
    """Logout user"""
    if 'user_license' in request.session:
        del request.session['user_license']
        del request.session['user_phone']
        del request.session['user_name']
    return redirect('login')


def user_dashboard(request):
    """User dashboard showing their vehicles and violations"""
    license_number = request.session.get('user_license')
    
    if not license_number:
        return redirect('login')
    
    # Get user's phone number from CustomUser
    try:
        custom_user = CustomUser.objects.get(license_number=license_number)
        user_phone = custom_user.phone
        user_name = custom_user.first_name
        
        # Get registered vehicles for this phone
        registered_vehicles = RegisteredUser.objects.filter(phone_number=user_phone)
        
        # Get all violations for these vehicles
        vehicle_numbers = [v.vehicle_number for v in registered_vehicles]
        violations = UserViolation.objects.filter(
            registered_user__in=registered_vehicles
        ).select_related('registered_user')
        
        context = {
            'user_name': user_name,
            'user_phone': user_phone,
            'user_license': license_number,
            'registered_vehicles': registered_vehicles,
            'violations': violations,
            'total_violations': violations.count(),
            'overspeeding_count': violations.filter(violation_type='overspeeding').count(),
            'no_helmet_count': violations.filter(violation_type='no_helmet').count()
        }
        
        return render(request, 'app/user_dashboard.html', context)
        
    except CustomUser.DoesNotExist:
        return redirect('login')


def clear_violations(request):
    """Clear all violations for the logged-in user after they acknowledge them"""
    license_number = request.session.get('user_license')
    if not license_number:
        return redirect('login')
    
    try:
        custom_user = CustomUser.objects.get(license_number=license_number)
        registered_vehicles = RegisteredUser.objects.filter(phone_number=custom_user.phone)
        UserViolation.objects.filter(registered_user__in=registered_vehicles).delete()
    except CustomUser.DoesNotExist:
        pass
        
    return redirect('user_dashboard')
def dashboard(request):
    email = request.session.get('user_email')
    context = {'email': email}
    return render(request, 'app/main.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from django.conf import settings
from .production_processor import process_video_file
from .forms import VehicleRegistrationForm
from .models import RegisteredUser
import json

@csrf_exempt
def process_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        
        # Save video temporarily
        temp_dir = os.path.join(settings.BASE_DIR, 'media', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        filename = f"{uuid.uuid4()}_{video_file.name}"
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)
                
        try:
            # Process the video using enhanced processor
            results = process_video_file(file_path)
            
            # Trigger vibration alerts for registered users
            violations = results.get('violations', [])
            if violations:
                # Make internal request to trigger alerts with detailed violation info
                alert_response = trigger_vibration_alert_internal(violations, video_file.name)
                results['alerts'] = alert_response
                
                # Save violations to database for registered users
                for violation in results.get('violations', []):
                    plate = normalize_plate(violation.get('plate'))
                    if plate and plate != 'UNREADABLE':
                        try:
                            registered_user = RegisteredUser.objects.get(
                                vehicle_number=plate,
                                is_active=True
                            )
                            
                            # Save the violation
                            UserViolation.objects.create(
                                registered_user=registered_user,
                                violation_type=violation['type'],
                                speed=violation.get('speed'),
                                plate_number=plate,
                                frame_time=violation.get('frame'),
                                severity=violation.get('severity', 'medium'),
                                video_file=video_file.name
                            )
                        except RegisteredUser.DoesNotExist:
                            pass  # Not a registered user, skip saving
            
            # Clean up the temp file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return JsonResponse({'status': 'success', 'data': results})
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def register_vehicle(request):
    """Register user's phone number and vehicle number for alerts"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            vehicle_number = normalize_plate(data.get('vehicle_number'))
            
            if not phone_number or not vehicle_number:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Phone number and vehicle number are required'
                }, status=400)
            
            # Check if vehicle is already registered with another phone
            existing_vehicle = RegisteredUser.objects.filter(
                vehicle_number=vehicle_number
            ).first()
            
            if existing_vehicle:
                return JsonResponse({
                    'status': 'error',
                    'message': f'This vehicle ({vehicle_number}) is already registered with phone {existing_vehicle.phone_number}',
                    'already_registered': True
                }, status=400)
            
            # Check if phone is already registered
            existing_phone = RegisteredUser.objects.filter(
                phone_number=phone_number
            ).first()
            
            if existing_phone:
                # Update existing registration
                existing_phone.vehicle_number = vehicle_number
                existing_phone.is_active = True
                existing_phone.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Vehicle updated successfully',
                    'vehicle_number': vehicle_number
                })
            else:
                # Create new registration
                user = RegisteredUser.objects.create(
                    phone_number=phone_number,
                    vehicle_number=vehicle_number
                )
                user.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Vehicle registered successfully',
                    'vehicle_number': vehicle_number
                })
                
        except Exception as e:
            error_message = str(e)
            if 'UNIQUE constraint failed' in error_message and 'vehicle_number' in error_message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This vehicle number is already registered. Each vehicle can only be registered once.'
                }, status=400)
            elif 'UNIQUE constraint failed' in error_message and 'phone_number' in error_message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This phone number is already registered. Please use a different number.'
                }, status=400)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Database error: {error_message}'
                }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


@csrf_exempt
def trigger_vibration_alert(request):
    """Send vibration alert to registered users whose vehicles violated rules"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            violating_plates = data.get('violating_plates', [])
            
            if not violating_plates:
                return JsonResponse({
                    'status': 'success',
                    'message': 'No violations detected',
                    'alerts_sent': 0
                })
            
            # Find matching registered users
            alerts_sent = []
            for plate in violating_plates:
                plate_clean = normalize_plate(plate)
                matched_users = RegisteredUser.objects.filter(
                    vehicle_number=plate_clean,
                    is_active=True
                )
                
                for user in matched_users:
                    alerts_sent.append({
                        'phone_number': user.phone_number,
                        'vehicle_number': user.vehicle_number,
                        'violation_plate': plate_clean
                    })
            
            # In a real system, you would send SMS/push notification here
            # For now, we'll just return the list for frontend to handle vibration
            
            return JsonResponse({
                'status': 'success',
                'message': f'Found {len(alerts_sent)} matching vehicles',
                'alerts': alerts_sent,
                'alerts_sent': len(alerts_sent)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)


def trigger_vibration_alert_internal(violations, video_filename=None):
    """Internal function to check for registered users and prepare alert data"""
    try:
        if not violations:
            return {
                'status': 'success',
                'message': 'No violations detected',
                'alerts_sent': 0,
                'matched_users': []
            }
        
        # Get channel layer for WebSocket notifications
        channel_layer = get_channel_layer()
        
        # Find matching registered users
        matched_users = []
        for violation in violations:
            plate = violation.get('plate')
            if not plate or plate == 'UNREADABLE':
                continue
                
            plate_clean = normalize_plate(plate)
            registered_users = RegisteredUser.objects.filter(
                vehicle_number=plate_clean,
                is_active=True
            )
            
            for user in registered_users:
                user_data = {
                    'phone_number': user.phone_number,
                    'vehicle_number': user.vehicle_number,
                    'violation_plate': plate_clean,
                    'violation_type': violation.get('type'),
                    'speed': violation.get('speed'),
                    'severity': violation.get('severity', 'medium')
                }
                matched_users.append(user_data)
                
                # Send real-time vibration notification via WebSocket
                # This will trigger vibration AND show the warning modal on the user's mobile device
                v_type_clean = violation.get('type', 'traffic_violation').replace('_', ' ').title()
                async_to_sync(channel_layer.group_send)(
                    f'vibration_{user.phone_number}',
                    {
                        'type': 'send_vibration_alert',
                        'violation_type': v_type_clean,
                        'plate_number': plate_clean,
                        'speed': violation.get('speed'),
                        'severity': violation.get('severity', 'medium'),
                        'message': f"{v_type_clean} detected for vehicle {plate_clean}!",
                        'timestamp': str(timezone.now())
                    }
                )
        
        return {
            'status': 'success',
            'message': f'Found {len(matched_users)} matching vehicles',
            'alerts_sent': len(matched_users),
            'matched_users': matched_users
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'alerts_sent': 0,
            'matched_users': []
        }
