from django.shortcuts import render

from .models import ComplianceChecker
from .serializers import ComplianceCheckerSerializer

from rest_framework import viewsets

# Create your views here.

class ComplianceCheckerViewSet(viewsets.ModelViewSet):
    queryset = ComplianceChecker.objects.all()
    serializer_class = ComplianceCheckerSerializer