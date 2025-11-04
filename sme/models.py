from django.db import models

# Create your models here.

TECH_ADOPTION_LEVELS = [
    ('None', 'None'),
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

# class SMEProfile(models.Model):
#     company_id = models.AutoField(primary_key=True)
#     business_name = models.CharField(max_length=255)
#     country = models.CharField(max_length=100)
#     sector = models.CharField(max_length=150)
#     employees = models.PositiveIntegerField(default=0, null=True, blank=True)
#     annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True)
#     tech_adoption_level = models.CharField(max_length=10, choices=TECH_ADOPTION_LEVELS, blank=True, null=True)
#     main_challenges = models.TextField(blank=True, null=True)
#     digital_tools_used = models.TextField(blank=True, null=True)
#     year_established = models.IntegerField(blank=True, null=True)
#     growth_last_year = models.IntegerField(blank=True, null=True)
#     funding_status = models.CharField(max_length=100, choices=FUNDING_STATUS, blank=True, null=True)
#     female_owned = models.BooleanField(blank=True, null=True)
#     remote_work_policy = models.CharField(max_length=10, choices=REMOTE_WORK_POLICIES, blank=True, null=True)
#     contact_email = models.EmailField(blank=True, null=True)
#     phone_number = models.CharField(max_length=20, blank=True, null=True)
#     business_size = models.CharField(max_length=50, blank=True, null=True)
#     ownership_type = models.CharField(max_length=150, blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#     registration_number = models.CharField(max_length=100, blank=True, null=True)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.business_name


class SMEProfile(models.Model):
    business_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    year_established = models.IntegerField(blank=True, null=True)
    employees = models.IntegerField(blank=True, null=True)
    business_size = models.CharField(max_length=50, blank=True, null=True)
    annual_revenue = models.FloatField(blank=True, null=True)
    growth_last_year = models.FloatField(blank=True, null=True)
    funding_status = models.CharField(max_length=100, blank=True, null=True)
    ownership_type = models.CharField(max_length=100, blank=True, null=True)
    female_owned = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)
    main_challenges = models.TextField(blank=True, null=True)
    digital_tools_used = models.TextField(blank=True, null=True)
    tech_adoption_level = models.CharField(max_length=100, blank=True, null=True)
    remote_work_policy = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
