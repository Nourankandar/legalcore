from django.db import models
from legalcore.settings import AUTH_USER_MODEL
from apps.contracts.models import Contract

class AuditLog(models.Model):
    choises=[
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]
    user =  models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='audit_logs'
        )
    contract = models.ForeignKey(
        Contract, 
        on_delete=models.SET_NULL, 
        related_name='audit_logs'
        )
    action = models.CharField(max_length=20, choices=choises)
    extra_Data = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
