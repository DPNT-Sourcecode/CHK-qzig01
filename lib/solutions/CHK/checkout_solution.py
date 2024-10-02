from dataclasses import dataclass
from typing import List


@dataclass
class LineItem:
    item: str
    price: int
    special_offer: str


def load_price_table() -> List[LineItem]:
    return [
        LineItem(item="A", price=50, special_offer="3A for 130"),
        LineItem(item="A", price=50, special_offer="3A for 130"),
        LineItem(item="A", price=50, special_offer="3A for 130"),
        LineItem(item="A", price=50, special_offer="3A for 130"),
    ]


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    raise NotImplementedError()

