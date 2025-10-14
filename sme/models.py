from django.db import models

# Create your models here.

TECH_ADOPTION_LEVELS = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

FUNDING_STATUS = [
    ('Bootstrapped', 'Bootstrapped'),
    ('Seed Funded', 'Seed Funded'),
    ('Series A', 'Series A'),
    ('Series B+', 'Series B+'),
]

REMOTE_WORK_POLICIES = [
    ('None', 'None'),
    ('Partial', 'Partial'),
    ('Full', 'Full'),
]

class SMEProfile(models.Model):
    company_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=150)
    employees = models.IntegerField()
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    tech_adoption_level = models.CharField(max_length=10, choices=TECH_ADOPTION_LEVELS)
    main_challenges = models.TextField()
    digital_tools_used = models.TextField()
    year_established = models.IntegerField()
    growth_last_year = models.IntegerField()
    funding_status = models.CharField(max_length=100, choices=FUNDING_STATUS)
    female_owned = models.BooleanField()
    remote_work_policy = models.CharField(max_length=10, choices=REMOTE_WORK_POLICIES)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    business_size = models.CharField(max_length=50)
    ownership_type = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.business_name