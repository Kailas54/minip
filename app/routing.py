"""
WebSocket Routing Configuration
Maps URL patterns to WebSocket consumers
"""

from django.urls import re_path
from app import websocket_consumer

websocket_urlpatterns = [
    # Vibration notification endpoint for individual users
    re_path(r'ws/notifications/(?P<phone>[^/]+)/$', websocket_consumer.VibrationNotificationConsumer.as_asgi()),
    
    # Broadcast endpoint for admin dashboards
    re_path(r'ws/violations/broadcast/$', websocket_consumer.ViolationBroadcastConsumer.as_asgi()),
]
