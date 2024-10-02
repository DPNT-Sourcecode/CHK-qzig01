from dataclasses import dataclass, field
from typing import List


@dataclass
class LineItem:
    item: str
    price: int
    special_offer: str = ""


@dataclass
class PriceTable:
    line_items: List[LineItem] = field(default_factory=list)


def load_price_table() -> List[LineItem]:
    return [
        LineItem(item="A", price=50, special_offer="3A for 130"),
        LineItem(item="B", price=30, special_offer="2B for 45"),
        LineItem(item="C", price=20),
        LineItem(item="D", price=15),
    ]


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    raise NotImplementedError()


