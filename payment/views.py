from rest_framework import mixins, viewsets

from .models import Account, Payment
from .serializers import AccountSerializer, PaymentSerializer


class AccountViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PaymentViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
