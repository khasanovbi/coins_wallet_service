from django.db.models import F
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Account, Payment


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "name", "balance", "currency")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "source_account",
            "destination_account",
            "amount",
            "currency",
            "created_datetime",
        )
        read_only_fields = ("currency",)

    def validate(self, data):
        source_account = data["source_account"]
        destination_account = data["destination_account"]
        if source_account.currency != destination_account.currency:
            raise serializers.ValidationError(
                _("only same currency payments are supported.")
            )

        if source_account.pk == destination_account.pk:
            raise serializers.ValidationError(
                _("source and destination accounts must not match.")
            )
        # NOTE: prevalidate amount to make less sql queries.
        self._validate_amount(source_account=source_account, amount=data["amount"])
        return data

    @staticmethod
    def _validate_amount(source_account, amount):
        if source_account.balance < amount:
            raise serializers.ValidationError(
                {"non_field_errors": [_("insufficient funds to make a payment.")]}
            )

    @atomic
    def create(self, validated_data):
        # NOTE: use select_for_update to prevent less than 0 amount
        source_account = Account.objects.select_for_update().get(
            pk=validated_data["source_account"].pk
        )
        amount = validated_data["amount"]
        self._validate_amount(source_account=source_account, amount=amount)

        destination_account = validated_data["destination_account"]
        Account.objects.filter(pk=source_account.pk).update(
            balance=F("balance") - amount
        )
        Account.objects.filter(pk=destination_account.pk).update(
            balance=F("balance") + amount
        )
        return Payment.objects.create(
            source_account=source_account,
            destination_account=destination_account,
            amount=amount,
            currency=source_account.currency,
        )
