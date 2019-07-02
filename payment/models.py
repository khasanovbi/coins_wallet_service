from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils.translation import ugettext_lazy as _


class CurrencyField(models.CharField):
    USD = "USD"
    CURRENCY_CHOICES = [(USD, "USD")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_length=3, choices=self.CURRENCY_CHOICES, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["choices"]
        return name, path, args, kwargs


class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)
    balance = models.DecimalField(
        max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )
    currency = CurrencyField()

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return self.name


class Payment(models.Model):
    from_account = models.ForeignKey(
        Account, related_name="to_payments", on_delete=models.PROTECT
    )
    to_account = models.ForeignKey(
        Account, related_name="from_payments", on_delete=models.PROTECT
    )
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    currency = CurrencyField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(from_account=F("to_account")),
                name="from_to_accounts_difference",
            )
        ]
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return (
            f"{self.id}:{self.amount} {self.currency} "
            f"{self.from_account} -> {self.to_account}"
        )
