from django.urls import path, include
from . import views

from rest_framework import routers

app_name = 'finance'

router = routers.DefaultRouter()
# router.register(r'profiles', views.FinanceProfileViewset)

urlpatterns = [
    # path('', views.index, name='index'),
    path('api/', include(router.urls)),
]