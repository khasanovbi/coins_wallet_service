from decimal import Decimal

import pytest
from django.urls import reverse
from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    has_length,
    is_not,
    only_contains,
)
from rest_framework import status

from wallet.models import Account, CurrencyField

from .utils import call_concurrently, quantize_balance

pytestmark = pytest.mark.django_db


@pytest.fixture
def source_account():
    return Account.objects.create(
        name="source_account_name", balance="100", currency=CurrencyField.USD
    )


@pytest.fixture
def destination_account():
    return Account.objects.create(
        name="destination_account_name", balance="200", currency=CurrencyField.USD
    )


@pytest.fixture
def another_currency_destination_account():
    return Account.objects.create(
        name="destination_account_name", balance="200", currency=CurrencyField.PHP
    )


@pytest.fixture(scope="session")
def create_payment_request_factory(api_client):
    def create_payment(data):
        return api_client.post(reverse("wallet:payment-list"), data)

    return create_payment


def make_create_payment_request_data(source_account, destination_account, amount="50"):
    return {
        "source_account": source_account.pk,
        "destination_account": destination_account.pk,
        "amount": amount,
    }


class TestCreatePayment:
    def test_valid(
        self, source_account, destination_account, create_payment_request_factory
    ):
        amount = source_account.balance
        data = make_create_payment_request_data(
            source_account, destination_account, amount
        )
        response = create_payment_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_201_CREATED), response.json()
        )
        data["amount"] = quantize_balance(data["amount"])
        assert_that(response.json(), has_entries(data))

        expected_source_account_balance = Decimal(source_account.balance) - Decimal(
            amount
        )
        expected_destination_account_balance = Decimal(
            destination_account.balance
        ) + Decimal(amount)

        source_account.refresh_from_db()
        destination_account.refresh_from_db()

        assert_that(source_account.balance, equal_to(expected_source_account_balance))
        assert_that(
            destination_account.balance, equal_to(expected_destination_account_balance)
        )

    def test_required_field(self, create_payment_request_factory):
        response = create_payment_request_factory(None)
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to(
                {
                    field: ["This field is required."]
                    for field in ("source_account", "destination_account", "amount")
                }
            ),
        )

    @pytest.mark.parametrize(
        "is_source_account",
        [True, False],
        ids=["unexpected_source_account", "unexpected_destination_account"],
    )
    def test_unexpected_account(
        self, create_payment_request_factory, account, is_source_account
    ):
        unexpected_id = 10000
        assert_that(account.id, is_not(unexpected_id))

        params = {"amount": "100"}
        if is_source_account:
            params.update(
                source_account=Account(id=unexpected_id), destination_account=account
            )
        else:
            params.update(
                source_account=account, destination_account=Account(id=unexpected_id)
            )

        response = create_payment_request_factory(
            make_create_payment_request_data(**params)
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        expected_error_field = (
            "source_account" if is_source_account else "destination_account"
        )
        assert_that(
            response.json(),
            equal_to(
                {
                    expected_error_field: [
                        f'Invalid pk "{unexpected_id}" - object does not exist.'
                    ]
                }
            ),
        )

    def test_source_destination_accounts_difference(
        self, create_payment_request_factory, account
    ):
        response = create_payment_request_factory(
            make_create_payment_request_data(
                source_account=account,
                destination_account=account,
                amount=account.balance,
            )
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to(
                {
                    "non_field_errors": [
                        "source and destination accounts must not match."
                    ]
                }
            ),
        )

    def test_different_currency_accounts(
        self,
        create_payment_request_factory,
        source_account,
        another_currency_destination_account,
    ):
        response = create_payment_request_factory(
            make_create_payment_request_data(
                source_account=source_account,
                destination_account=another_currency_destination_account,
                amount=source_account.balance,
            )
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to(
                {"non_field_errors": ["only same currency payments are supported."]}
            ),
        )

    def test_insufficient_balance_of_source_account(
        self, create_payment_request_factory, source_account, destination_account
    ):
        response = create_payment_request_factory(
            make_create_payment_request_data(
                source_account=source_account,
                destination_account=destination_account,
                amount=Decimal(source_account.balance) + 1,
            )
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(
            response.json(),
            equal_to({"non_field_errors": ["insufficient funds to make a payment."]}),
        )

    @pytest.mark.parametrize(
        "amount, error",
        [
            ("-0.1", "Ensure this value is greater than or equal to 0.01."),
            ("0", "Ensure this value is greater than or equal to 0.01."),
            ("10.123", "Ensure that there are no more than 2 decimal places."),
        ],
    )
    def test_invalid_amount(
        self,
        create_payment_request_factory,
        source_account,
        destination_account,
        amount,
        error,
    ):
        response = create_payment_request_factory(
            make_create_payment_request_data(
                source_account=source_account,
                destination_account=destination_account,
                amount=amount,
            )
        )
        assert_that(
            response.status_code, equal_to(status.HTTP_400_BAD_REQUEST), response.json()
        )
        assert_that(response.json(), equal_to({"amount": [error]}))

    @pytest.mark.parametrize("amount", ["0.01", "100"])
    def test_valid_amount(
        self,
        create_payment_request_factory,
        source_account,
        destination_account,
        amount,
    ):
        data = make_create_payment_request_data(
            source_account=source_account,
            destination_account=destination_account,
            amount=amount,
        )
        response = create_payment_request_factory(data)
        assert_that(
            response.status_code, equal_to(status.HTTP_201_CREATED), response.json()
        )
        data["amount"] = quantize_balance(data["amount"])
        assert_that(response.json(), has_entries(data))


@pytest.mark.django_db(transaction=True)
def test_stress_multiple_payments_from_one_source_account_balance(
    create_payment_request_factory, destination_account
):
    balance = 100
    payment_amount = 5
    source_account = Account.objects.create(
        name="source_account_name", balance=balance, currency=CurrencyField.USD
    )
    data = make_create_payment_request_data(
        source_account=source_account,
        destination_account=destination_account,
        amount=str(payment_amount),
    )

    concurrent_calls_count = 30
    futures = call_concurrently(
        concurrency=concurrent_calls_count,
        calls_count=concurrent_calls_count,
        target=create_payment_request_factory,
        args=(data,),
    )
    responses = (future.result() for future in futures)

    failed_responses = [
        response
        for response in responses
        if response.status_code != status.HTTP_201_CREATED
    ]
    expected_failed_responses_count = concurrent_calls_count - balance / payment_amount
    assert_that(failed_responses, has_length(expected_failed_responses_count))
    assert_that(
        [response.json() for response in failed_responses],
        only_contains(
            equal_to({"non_field_errors": ["insufficient funds to make a payment."]})
        ),
    )
