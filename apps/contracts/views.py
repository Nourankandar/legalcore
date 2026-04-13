from django.shortcuts import render
from rest_framework import viewsets
from .seralizers import ContractSerializer,UplodeFiles
from .models import Contract
from apps.accounts.permissions import IsAdminOrLawyer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action

class ContractViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminOrLawyer]
    queryset = Contract.objects.filter(deleted_at__isnull=True)
    serializer_class = ContractSerializer

    def get_queryset(self):
        Contract.objects.filter(
            deadline__lte=timezone.now().date(),
            status='ACTIVE'
        ).update(status='EXPIRED')

        user = self.request.user
        if user.role in ['ADMIN', 'LAWYER'] or user.is_superuser:
            queryset = Contract.objects.filter(deleted_at__isnull=True)
        else:
            queryset= Contract.objects.filter(parties=user)
        
        status_para = self.request.query_params.get('status')
        if status_para: 
            queryset = queryset.filter(status=status_para)
        
        deadline_before = self.request.query_params.get('deadline_before')
        if deadline_before:
            queryset = queryset.filter(deadline__lte=deadline_before)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.created_by = self.request.user
        instance.deleted_at = timezone.now()
        instance.save()
    
    @action(detail=True,methods = ['POST'])
    def uplode(self,request,pk=None):
        contract = self.get_object()
        seralizer = UplodeFiles(contract,data = request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response({'status': 'File uploaded successfully'})
        else:
            return Response(seralizer.errors,status=400)

