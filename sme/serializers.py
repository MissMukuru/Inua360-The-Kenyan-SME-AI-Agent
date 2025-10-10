from rest_framework import serializers
from sme.models import SMEProfile

class SMEProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMEProfile
        fields = '__all__'