from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q
from django.utils.translation import ugettext_lazy as _


class CurrencyField(models.CharField):
    USD = "USD"
    PHP = "PHP"
    CHOICES = [(USD, _("United States dollar")), (PHP, _("Philippine peso"))]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, max_length=3, choices=self.CHOICES, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["choices"]
        return name, path, args, kwargs


class Account(models.Model):
    name = models.CharField(
        max_length=50, unique=True, help_text=_("unique name of account")
    )
    balance = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        help_text=_("amount of money in account"),
    )
    currency = CurrencyField(help_text=_("money currency of account"))

    class Meta:
        constraints = [
            CheckConstraint(check=Q(balance__gte=0), name="nonnegative_balance")
        ]
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return self.name


class Payment(models.Model):
    created_datetime = models.DateTimeField(
        auto_now_add=True, help_text=_("time of payment")
    )
    source_account = models.ForeignKey(
        Account,
        related_name="outgoing_payments",
        on_delete=models.PROTECT,
        help_text=_("account from which money comes"),
    )
    destination_account = models.ForeignKey(
        Account,
        related_name="incoming_payments",
        on_delete=models.PROTECT,
        help_text=_("account to which money comes"),
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("payment amount"),
    )
    currency = CurrencyField(help_text=_("money currency of payment"))

    class Meta:
        constraints = [
            CheckConstraint(
                check=~Q(source_account=F("destination_account")),
                name="source_destination_accounts_difference",
            ),
            CheckConstraint(check=Q(amount__gt=0), name="positive_amount"),
        ]
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return (
            f"{self.id}:{self.amount} {self.currency} "
            f"{self.source_account} -> {self.destination_account}"
        )
