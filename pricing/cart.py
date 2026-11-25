from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

TAX_RATE = Decimal("0.08")


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class LineItem:
    sku: str
    unit_price: Decimal
    quantity: int = 1

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise ValueError("quantity must be at least 1")
        if self.unit_price < 0:
            raise ValueError("unit_price cannot be negative")

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Cart:
    items: list[LineItem] = field(default_factory=list)

    def add(self, sku: str, unit_price: str | Decimal, quantity: int = 1) -> None:
        self.items.append(LineItem(sku, Decimal(unit_price), quantity))

    def subtotal(self) -> Decimal:
        return _money(sum((item.subtotal for item in self.items), Decimal("0")))

    def tax(self) -> Decimal:
        return _money(self.subtotal() * TAX_RATE)

    def total(self) -> Decimal:
        return _money(self.subtotal() + self.tax())
