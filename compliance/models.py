from django.db import models

# from ..sme.models import SMEProfile
from sme.models import SMEProfile

# Create your models here.

class ComplianceChecker(models.Model):
    business_type = models.CharField(max_length=255)
    compliance_status = models.CharField(max_length=100)
    last_checked = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)

    business_registration_certificate = models.FileField(upload_to='compliance_docs/', blank=True, null=True)
    tax_compliance_certificate = models.FileField(upload_to='compliance_docs/', blank=True, null=True)
    health_safety_certificate = models.FileField(upload_to='compliance_docs/', blank=True, null=True)
    environmental_clearance = models.FileField(upload_to='compliance_docs/', blank=True, null=True)
    single_business_permit = models.FileField(upload_to='compliance_docs/', blank=True, null=True)
    fire_safety_certificate = models.FileField(upload_to='compliance_docs/', blank=True, null=True)

    def __str__(self):
        return f"{self.business_type} - {self.compliance_status}"
    
class Document(models.Model):
    DOCUMENT_TYPES = [
        ("business_registration", "Business Registration Certificate"),
        ("kra_pin", "KRA PIN Certificate"),
        ("county_permit", "County Business Permit"),
        ("nssf", "NSSF Registration"),
        ("nhif", "NHIF Registration"),
        ("tax_compliance", "Tax Compliance Certificate"),
    ]

    profile = models.ForeignKey(SMEProfile, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="compliance_docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.business_name} - {self.document_type}"
    
class ValidationResult(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="validation_result")
    valid = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    recommendations = models.JSONField(blank=True, null=True)
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Valid" if self.valid else "Needs Review"
        return f"{self.document.document_type} - {status}"
    
class ComplianceChecker(models.Model):
    profile = models.OneToOneField(SMEProfile, on_delete=models.CASCADE, related_name="compliance_summary")
    overall_status = models.CharField(max_length=100, default="Pending")
    last_checked = models.DateTimeField(auto_now=True)
    completion_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.profile.business_name} - {self.overall_status}"