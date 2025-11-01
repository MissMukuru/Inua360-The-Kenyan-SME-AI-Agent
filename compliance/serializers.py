from rest_framework import serializers
from .models import ComplianceChecker, Document, ValidationResult

class ComplianceCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceChecker
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class ValidationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationResult
        fields = '__all__'

class GeminiRequestSerializer(serializers.ModelSerializer):
    prompt = serializers.CharField(required=False, allow_blank=False)
    image = serializers.ImageField(required=False)

class GeminiValidationSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    prompt = serializers.CharField(required=False, allow_blank=True)