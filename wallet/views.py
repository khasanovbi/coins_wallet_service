from rest_framework import mixins, viewsets

from .models import Account, Payment
from .serializers import AccountSerializer, PaymentSerializer


class AccountViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    create:
    Create a new account instance.

    retrieve:
    Return the given account.

    list:
    Return a list of all the existing accounts.

    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PaymentViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    create:
    Create a new payment instance.

    list:
    Return a list of all the existing payments.
    """

    filterset_fields = ("source_account", "destination_account")
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
