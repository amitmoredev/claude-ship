from decimal import Decimal

import pytest

from pricing import Cart, LineItem


def test_empty_cart_totals_zero():
    cart = Cart()
    assert cart.total() == Decimal("0.00")


def test_subtotal_tax_and_total():
    cart = Cart()
    cart.add("BOOK", "10.00", 2)
    cart.add("PEN", "1.50")
    assert cart.subtotal() == Decimal("21.50")
    assert cart.tax() == Decimal("1.72")
    assert cart.total() == Decimal("23.22")


def test_rejects_bad_quantity():
    with pytest.raises(ValueError):
        LineItem("BOOK", Decimal("10.00"), 0)
