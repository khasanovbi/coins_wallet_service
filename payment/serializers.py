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
        fields = ("id", "from_account", "to_account", "amount", "currency")

    def validate(self, data):
        from_account = data["from_account"]
        to_account = data["to_account"]
        if from_account.currency != to_account.currency:
            raise serializers.ValidationError(
                _("only same currency payments are supported.")
            )

        if from_account.pk == to_account.pk:
            raise serializers.ValidationError(
                _("source and destination accounts must not match.")
            )
        # NOTE: prevalidate amount to make less sql queries.
        self._validate_amount(from_account=from_account, amount=data["amount"])
        return data

    @staticmethod
    def _validate_amount(from_account, amount):
        if from_account.balance < amount:
            raise serializers.ValidationError(
                {"non_field_errors": [_("insufficient funds to make a payment.")]}
            )

    @atomic
    def create(self, validated_data):
        # NOTE: use select_for_update to prevent less than 0 amount
        from_account = Account.objects.select_for_update().get(
            pk=validated_data["from_account"].pk
        )
        amount = validated_data["amount"]
        self._validate_amount(from_account=from_account, amount=amount)

        to_account = validated_data["to_account"]
        Account.objects.filter(pk=from_account.pk).update(balance=F("balance") - amount)
        Account.objects.filter(pk=to_account.pk).update(balance=F("balance") + amount)
        return Payment.objects.create(
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            currency=from_account.currency,
        )
