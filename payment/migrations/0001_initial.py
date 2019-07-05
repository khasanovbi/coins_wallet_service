# Generated by Django 2.2.3 on 2019-07-04 22:21

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import django.db.models.expressions
from django.db import migrations, models

import payment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=19,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0"))
                        ],
                    ),
                ),
                ("currency", payment.models.CurrencyField()),
            ],
            options={"verbose_name": "account", "verbose_name_plural": "accounts"},
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=19)),
                ("currency", payment.models.CurrencyField()),
                (
                    "destination_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="incoming_payments",
                        to="payment.Account",
                    ),
                ),
                (
                    "source_account",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="outgoing_payments",
                        to="payment.Account",
                    ),
                ),
            ],
            options={"verbose_name": "payment", "verbose_name_plural": "payments"},
        ),
        migrations.AddConstraint(
            model_name="account",
            constraint=models.CheckConstraint(
                check=models.Q(balance__gte=0), name="nonnegative_balance"
            ),
        ),
        migrations.AddConstraint(
            model_name="payment",
            constraint=models.CheckConstraint(
                check=models.Q(
                    _negated=True,
                    source_account=django.db.models.expressions.F(
                        "destination_account"
                    ),
                ),
                name="source_destination_accounts_difference",
            ),
        ),
    ]
