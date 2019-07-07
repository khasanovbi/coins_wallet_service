import pytest
from django.urls import reverse
from hamcrest import assert_that, empty, equal_to, has_entries, has_item, is_not
from rest_framework import status

from wallet.models import CurrencyField

from .utils import quantize_balance

pytestmark = pytest.mark.django_db


def make_create_account_request_data(
    name="account_name", balance="123.45", currency=CurrencyField.USD
):
    return {"name": name, "balance": balance, "currency": currency}


class TestCreateAccount:
    @pytest.fixture(scope="session")
    def create_account_request_factory(self, api_client):
        def create_account(data):
            return api_client.post(reverse("wallet:account-list"), data)

        return create_account

    def test_valid(self, create_account_request_factory):
        data = make_create_account_request_data()
        response = create_account_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_201_CREATED), response.json()
        )
        assert_that(response.json(), has_entries(data))

    def test_required_fields(self, create_account_request_factory):
        response = create_account_request_factory(None)
        assert_that(response.status_code, equal_to(status.HTTP_400_BAD_REQUEST))
        assert_that(
            response.json(),
            equal_to(
                {
                    field: ["This field is required."]
                    for field in ("name", "balance", "currency")
                }
            ),
        )

    @pytest.mark.parametrize("balance", ["0", "1.12", "100"])
    def test_valid_balance(self, create_account_request_factory, balance):
        data = make_create_account_request_data(balance=balance)
        response = create_account_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_201_CREATED), response.json()
        )
        data["balance"] = quantize_balance(data["balance"])

        assert_that(response.json(), has_entries(data))

    @pytest.mark.parametrize(
        "balance, error",
        [
            ("-1", "Ensure this value is greater than or equal to 0."),
            ("10.1234", "Ensure that there are no more than 2 decimal places."),
        ],
    )
    def test_invalid_balance(self, create_account_request_factory, balance, error):
        response = create_account_request_factory(
            make_create_account_request_data(balance=balance)
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(response.json(), equal_to({"balance": [error]}))

    def test_too_long_name(self, create_account_request_factory):
        response = create_account_request_factory(
            make_create_account_request_data(name="a" * 1000)
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to({"name": ["Ensure this field has no more than 50 characters."]}),
        )

    def test_nonunique_name(self, account, create_account_request_factory):
        data = make_create_account_request_data(name=account.name)
        response = create_account_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to({"name": ["account with this name already exists."]}),
        )

    def test_unexpected_currency(self, create_account_request_factory):
        unexpected_currency = "Unexpected currency"
        assert_that(dict(CurrencyField.CHOICES), is_not(has_item(unexpected_currency)))
        data = make_create_account_request_data(currency=unexpected_currency)
        response = create_account_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to({"currency": [f'"{unexpected_currency}" is not a valid choice.']}),
        )


class TestListAccounts:
    @pytest.fixture(scope="session")
    def list_accounts_request_factory(self, api_client):
        def list_accounts():
            return api_client.get(reverse("wallet:account-list"))

        return list_accounts

    def test_zero_account_list(self, list_accounts_request_factory):
        response = list_accounts_request_factory()
        assert_that(response.status_code, equal_to(status.HTTP_200_OK), response.json())
        assert_that(response.json(), empty())

    def test_some_account_list(self, list_accounts_request_factory, account):
        response = list_accounts_request_factory()
        assert_that(response.status_code, equal_to(status.HTTP_200_OK), response.json())
        expected_response = [
            {
                "id": account.id,
                "name": account.name,
                "balance": quantize_balance(account.balance),
                "currency": account.currency,
            }
        ]
        assert_that(response.json(), equal_to(expected_response))
