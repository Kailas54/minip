"""
URL configuration for platevision project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('test/', lambda request: __import__('django.shortcuts').shortcuts.render(request, 'app/test.html'), name='test'),
    path('login/',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.user_dashboard,name='user_dashboard'),
    path('clear-violations/', views.clear_violations, name='clear_violations'),
    path('main/',views.dashboard,name='dashboard'),
    path('process-video/', views.process_video, name='process_video'),
    path('register-vehicle/', views.register_vehicle, name='register_vehicle'),
    path('trigger-alert/', views.trigger_vibration_alert, name='trigger_alert'),
]
