from django.shortcuts import render
from rest_framework.views import APIView, Response
from .serializers import AuditLogsSerializers
from .models import AuditLog
from apps.accounts.permissions import IsAdmin
from .paginator import AuditLogPagination


class AuditLogsView(APIView):
    permission_classes = [IsAdmin]
    serializer_class = AuditLogsSerializers
    queryset = AuditLog.objects.all()

    def get(self, request):
        queryset = AuditLog.objects.all().order_by('-timestamp')


        contract_id = self.request.query_params.get('contract_id')
        if contract_id: 
            queryset = queryset.filter(contract_id=contract_id)
        
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        action = self.request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)

        paginator = AuditLogPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = AuditLogsSerializers(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = AuditLogsSerializers(queryset, many=True)
        return Response(serializer.data)
    