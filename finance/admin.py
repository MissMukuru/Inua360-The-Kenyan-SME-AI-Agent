from django.contrib import admin

from .models import FinancialAnalytics, FinancialRecord, ExpenseCategory

# Register your models here.

admin.site.register(FinancialAnalytics)
admin.site.register(FinancialRecord)
admin.site.register(ExpenseCategory)