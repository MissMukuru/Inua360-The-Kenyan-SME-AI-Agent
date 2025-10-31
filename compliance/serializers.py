from rest_framework import serializers
from .models import ComplianceChecker

class ComplianceCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceChecker
        fields = '__all__'

class GeminiRequestSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(required=False, allow_blank=False)
    image = serializers.ImageField(required=False)