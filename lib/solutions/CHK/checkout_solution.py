from dataclasses import dataclass, field
from typing import Dict, List


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
    special_offer: SpecialOffer = field(default_factory=SpecialOffer)

    @property
    def has_special_offer(self) -> bool:
        return self.special_offer.has_offer

    def get_value(self, count: int):
        if self.has_special_offer:
            if count >= self.special_offer.multiple:
                return self.special_offer.price
        return self.price * count

    @classmethod
    def new(cls, line_item_id: str, price: int, special_offer_str: str = None):
        return cls(
            price=price,
            special_offer=SpecialOffer.new(line_item_id, special_offer_str or ""),
        )


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
            "A": LineItemData.new("A", price=50, special_offer_str="3A for 130"),
            "B": LineItemData.new("B", price=30, special_offer_str="2B for 45"),
            "C": LineItemData.new("C", price=20),
            "D": LineItemData.new("D", price=15),
        }
    )


def compute_checkout_value(price_table: PriceTable, items: Dict[str, int]) -> int:
    checkout_value = 0
    for item, count in items.items():
        line_item = price_table.get_data_for(item)
        print(count, line_item)
        checkout_value += line_item.get_value(count)
    return checkout_value


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus: List[str]) -> int:
    price_table = load_price_table()
    items_found = {}
    for sku in skus:
        if not price_table.line_item_in_table(sku):
            return -1
        if sku not in items_found:
            items_found[sku] = 0
        items_found[sku] += 1

    print(items_found)
    return compute_checkout_value(price_table, items_found)








