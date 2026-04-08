from django.shortcuts import render
from rest_framework import viewsets, permissions
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class NotificationViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'patch', 'head', 'options']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer


    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user,is_read=False).order_by('-created_at').select_related('contract')
    

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def read_notification(self,request,pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'Notification marked as read'})
    
    
