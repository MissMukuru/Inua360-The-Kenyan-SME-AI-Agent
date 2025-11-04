from rest_framework import serializers
from sme.models import SMEProfile

class SMEProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMEProfile
        fields = '__all__'
        extra_kwargs = {
            'year_established': {'required': False, 'allow_null': True},
            'employees': {'required': False, 'allow_null': True},
            'business_size': {'required': False, 'allow_null': True},
            'annual_revenue': {'required': False, 'allow_null': True},
            'growth_last_year': {'required': False, 'allow_null': True},
            'funding_status': {'required': False, 'allow_null': True},
            'ownership_type': {'required': False, 'allow_null': True},
            'location': {'required': False, 'allow_null': True},
            'main_challenges': {'required': False, 'allow_null': True},
            'digital_tools_used': {'required': False, 'allow_null': True},
            'tech_adoption_level': {'required': False, 'allow_null': True},
            'remote_work_policy': {'required': False, 'allow_null': True},
        }