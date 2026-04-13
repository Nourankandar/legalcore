from rest_framework import serializers
from .models import AuditLog
class AuditLogsSerializers(serializers.ModelSerializer):
    contract_title = serializers.CharField(source='contract.title', read_only=True)
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'extra_data', 'timestamp', 'contract_title']