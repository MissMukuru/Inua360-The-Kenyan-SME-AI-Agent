from django.db import models

from sme.models import SMEProfile

# Create your models here.

class FinancialRecord(models.Model):
    sme = models.ForeignKey(SMEProfile, on_delete=models.CASCADE, related_name='financial_records')
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    financial_goals = models.TextField(blank=True, null=True)
    cash_flow = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    savings_rate = models.FloatField(null=True, blank=True)
    health_score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sme.business_name} - Financial Record ({self.created_at.date()})"

class ExpenseCategory(models.Model):
    financial_record = models.ForeignKey(FinancialRecord, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.category} - {self.amount}"

class FinancialAnalytics(models.Model):
    sme = models.OneToOneField(SMEProfile, on_delete=models.CASCADE, related_name='financial_analytics')
    profit_margin = models.FloatField(default=0)
    expense_ratio = models.FloatField(default=0)
    employee_efficiency = models.FloatField(default=0)
    financial_health_index = models.FloatField(default=0)
    market_resilience = models.FloatField(default=0)
    funding_stage = models.CharField(max_length=100, blank=True, null=True)
    revenue_growth_rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Financial Analytics - {self.sme.business_name}"
