from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import viewsets

from sme.models import SMEProfile
from sme.serializers import SMEProfileSerializer

# Create your views here.

def index(request):
    return HttpResponse("<h1 style='color:blue; text-align:center;'>Inua360</h1>")

class SMEProfileViewset(viewsets.ModelViewSet):
    queryset = SMEProfile.objects.all()
    serializer_class = SMEProfileSerializer