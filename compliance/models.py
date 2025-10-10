from django.db import models

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