"""
WebSocket Server for Real-time Vibration Notifications
This module handles real-time communication between the backend and mobile browsers
"""

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class VibrationNotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for sending real-time vibration alerts to mobile devices
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        # Get user's phone number from URL query params
        self.phone_number = self.scope['url_route']['kwargs']['phone']
        self.user_name = self.scope['query_string'].decode()
        
        # Create a unique room name for each user based on phone number
        self.room_group_name = f'vibration_{self.phone_number}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send confirmation to client
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected to vibration notification service',
            'phone': self.phone_number
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket
        Currently used for heartbeat/keepalive
        """
        try:
            data = json.loads(text_data)
            
            # Handle heartbeat/ping
            if data.get('type') == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
                
        except json.JSONDecodeError:
            pass
    
    async def send_vibration_alert(self, event):
        """
        Send vibration alert to WebSocket
        This method is called when a violation is detected
        """
        # Extract data from event
        violation_type = event.get('violation_type', 'unknown')
        plate_number = event.get('plate_number', 'UNKNOWN')
        speed = event.get('speed')
        severity = event.get('severity', 'medium')
        timestamp = event.get('timestamp')
        
        # Create vibration pattern based on severity
        vibration_pattern = self.get_vibration_pattern(severity, violation_type)
        
        # Send vibration command to client
        await self.send(text_data=json.dumps({
            'type': 'vibration_alert',
            'violation_type': violation_type,
            'plate_number': plate_number,
            'speed': speed,
            'severity': severity,
            'timestamp': timestamp,
            'vibration_pattern': vibration_pattern,
            'message': f'{violation_type.replace("_", " ").title()} detected for vehicle {plate_number}'
        }))
    
    def get_vibration_pattern(self, severity, violation_type):
        """
        Generate vibration pattern based on violation severity and type
        
        Returns array of [on, off, on, off, ...] in milliseconds
        """
        if severity == 'high':
            # Strong alert: 3 long vibrations
            return [500, 200, 500, 200, 500]
        elif severity == 'medium':
            # Medium alert: 2 medium vibrations
            return [400, 200, 400]
        else:
            # Low alert: 1 short vibration
            return [300]


class ViolationBroadcastConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for broadcasting violations to all connected admin dashboards
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.room_group_name = 'violations_broadcast'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send confirmation
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'message': 'Connected to violation broadcast'
        }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def broadcast_violation(self, event):
        """Broadcast violation to all connected clients"""
        await self.send(text_data=json.dumps({
            'type': 'new_violation',
            'data': event.get('data')
        }))
