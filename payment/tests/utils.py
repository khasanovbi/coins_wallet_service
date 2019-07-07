from decimal import Decimal


def quantize_balance(balance, digits=2):
    return str(Decimal(balance).quantize(Decimal("1." + "0" * digits)))
