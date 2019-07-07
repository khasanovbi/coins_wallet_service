import pytest
from rest_framework.test import APIClient

from payment.models import Account, CurrencyField


@pytest.fixture(scope="session")
def api_client():
    return APIClient()


@pytest.fixture
def account():
    return Account.objects.create(
        name="account_name", balance="100", currency=CurrencyField.USD
    )
