from dataclasses import dataclass, field
from typing import Dict


@dataclass
class LineItemData:

    price: int
    special_offer: str = ""


@dataclass
class PriceTable:
    line_items: Dict[str, LineItemData] = field(default_factory=dict)

    @property
    def count_items(self):
        return len(self.line_items)


def load_price_table() -> PriceTable:
    return PriceTable(
        line_items={
            "A": LineItemData(price=50, special_offer="3A for 130"),
            "B": LineItemData(price=30, special_offer="2B for 45"),
            "C": LineItemData(price=20),
            "D": LineItemData(price=15),
        }
    )


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    raise NotImplementedError()



