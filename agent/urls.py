from django.urls import path, include
from . import views

from rest_framework import routers

app_name = 'agent'

router = routers.DefaultRouter()
# router.register(r'profiles', views.AgentProfileViewset)

urlpatterns = [
    # path('', views.index, name='index'),
    path('api/', include(router.urls)),
]