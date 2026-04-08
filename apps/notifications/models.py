from django.db import models
from legalcore.settings import AUTH_USER_MODEL
from apps.contracts.models import Contract

class Notification(models.Model):
    recipient = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
        )
    contract = models.ForeignKey(
        Contract, 
        on_delete=models.CASCADE, 
        related_name='notifications'
        )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message}"