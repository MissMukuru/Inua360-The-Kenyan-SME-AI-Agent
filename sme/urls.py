from django.urls import path, include
from . import views

from rest_framework import routers

app_name = 'sme'

router = routers.DefaultRouter()
router.register(r'profiles', views.SMEProfileViewset)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
]
