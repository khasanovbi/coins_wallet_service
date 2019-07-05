from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from .apps import PaymentConfig
from .views import AccountViewSet, PaymentViewSet

router = routers.DefaultRouter()
router.register(r"accounts", AccountViewSet)
router.register(r"payments", PaymentViewSet)

app_name = PaymentConfig.name
urlpatterns = [url(r"^/", include(router.urls))]
