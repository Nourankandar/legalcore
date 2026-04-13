from django.urls import path
from .views import AuditLogsView

urlpatterns = [
    path('auditLog/', AuditLogsView.as_view(), name='audit_logs'),
]