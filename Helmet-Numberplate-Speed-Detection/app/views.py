from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from django.shortcuts import redirect


def home(request):
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        adharcard = request.POST.get('adharcard')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        # hashed_password = make_password(password)

        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            address=address,
            adharcard=adharcard,
            phone=phone,
            age=age
        )
        user.save()
        return redirect('dashboard')
    return render(request, 'app/register.html')




def dashboard(request):
    email = request.session.get('user_email')
    context = {'email': email}
    return render(request, 'app/main.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
from django.conf import settings
from .video_processor import process_video_file

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
            # Process the video
            results = process_video_file(file_path)
            
            # Clean up the temp file after processing
            if os.path.exists(file_path):
                os.remove(file_path)
                
            return JsonResponse({'status': 'success', 'data': results})
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
