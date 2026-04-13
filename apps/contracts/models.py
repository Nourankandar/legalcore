from django.utils import timezone

from django.db import models
from django.core.validators import FileExtensionValidator
from legalcore.settings import AUTH_USER_MODEL

class Contract(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('ARCHIVED', 'Archived'),
    ]
    title = models.CharField(max_length=255)
    arabic_title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    parties= models.ManyToManyField(AUTH_USER_MODEL,related_name='involved_contracts')
    created_by=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_contract')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    document = models.FileField(upload_to='Files/contracts/', null=True, blank=True,validators=[FileExtensionValidator(allowed_extensions=['pdf','docx'])])
    deleted_at = models.DateTimeField(null=True, blank=True)


    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    
        