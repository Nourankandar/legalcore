from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'contract', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')