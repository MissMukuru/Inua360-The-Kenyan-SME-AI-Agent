from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

app_name = "compliance"

router = DefaultRouter()

router.register(r'compliance-records', views.ComplianceCheckerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
