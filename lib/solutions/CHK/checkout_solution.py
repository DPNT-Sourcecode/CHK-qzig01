from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SpecialOffer:
    special_offer_str: str = ""
    price: int = 0
    multiple: int = 0

    @property
    def has_offer(self):
        return self.price != 0 and self.multiple != 0

    @classmethod
    def new(cls, line_item_id: str, sos: str):
        if sos == "":
            return cls()
        if line_item_id not in sos:
            raise Exception("invalid")
        tokens = sos.split(" for ")
        multiple = int(tokens[0].replace(line_item_id, ""))
        price = int(tokens[1])
        return cls(special_offer_str=sos, price=price, multiple=multiple)


@dataclass
class LineItemData:

    price: int
    special_offer: str = ""


@dataclass
class PriceTable:
    line_items: Dict[str, LineItemData] = field(default_factory=dict)

    def line_item_in_table(self, line_item_id: str) -> bool:
        if line_item_id in self.line_items:
            return True
        return False

    def get_data_for(self, line_item_id: str) -> LineItemData:
        if self.line_item_in_table(line_item_id):
            return self.line_items[line_item_id]
        raise Exception(f"line item id not in price table {line_item_id}")

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

