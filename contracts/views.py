from django.shortcuts import render
from rest_framework import viewsets
from .seralizers import ContractSerializer,UplodeFiles
from .models import Contract
from ..accounts.permissions import IsAdminOrLawyer
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class ContractViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminOrLawyer]
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get_queryset(self):
        Contract.objects.filter(
            deadline__lte=timezone.now().date(),
            status='ACTIVE'
        ).update(status='EXPIRED')

        user = self.request.user
        if user.role in ['ADMIN', 'LAWYER']:
            return Contract.objects.all()
        return Contract.objects.filter(parties=user)
        
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UplodeView(APIView):
    def post(self,request):
        serializer = UplodeFiles(data = request.data)
        if (serializer.is_valid(raise_exception=True)):
            return Response('Uplode Successfully', status=201)
        return Response('the file not allowed')
        
