from django.contrib import admin

from .models import ComplianceChecker, Document, ValidationResult

# Register your models here.

admin.site.register(ComplianceChecker)
admin.site.register(Document)
admin.site.register(ValidationResult)