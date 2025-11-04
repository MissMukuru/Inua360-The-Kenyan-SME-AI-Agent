from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status, viewsets
from rest_framework.response import Response

from sme.models import SMEProfile
from sme.serializers import SMEProfileSerializer

# Create your views here.

def index(request):
    return HttpResponse("<h1 style='color:blue; text-align:center;'>Inua360</h1>")

class SMEProfileViewset(viewsets.ModelViewSet):
    queryset = SMEProfile.objects.all()
    serializer_class = SMEProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Serializer errors:", serializer.errors)  # Log detailed errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)