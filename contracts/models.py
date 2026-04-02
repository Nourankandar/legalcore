from django.db import models
from ..accounts.models import User
from django.core.validators import FileExtensionValidator
from ..legalcore.settings import AUTH_USER_MODEL
# from django.utils import timezone

class Contract(models.Model):
    validators=[FileExtensionValidator(allowed_extensions=['pdf','docx'])]
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('ARCHIVED', 'Archived'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    parties= models.ManyToManyField(AUTH_USER_MODEL,related_name='involved_contracts')
    created_by=models.ForeignKey(AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='created_contract')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    document = models.FileField(upload_to='Files/contracts/', null=True, blank=True,validators=[FileExtensionValidator(allowed_extensions=['pdf','docx'])])

    # @property
    # def is_expired(self):
    #     if timezone.now().date()> self.deadline:
    #         return 'Expired'
    #     return self.status
    

        