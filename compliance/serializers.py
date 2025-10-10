from rest_framework import serializers
from .models import ComplianceChecker

class ComplianceCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceChecker
        fields = '__all__'