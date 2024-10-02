from dataclasses import dataclass, field
from typing import Dict, List
from lib.solutions.CHK.special_offer import Discount, new_special_offers


@dataclass
class LineItemData:

    price: int
    discounts: List[Discount] = field(default_factory=list)

    @property
    def has_special_offer(self) -> bool:
        return len(self.discounts) > 0

    def get_value(self, count: int):
        if self.has_special_offer:
            discounted_value = 0
            rem = count
            for so in self.discounts:
                if rem >= so.multiple:
                    special_offer_value, remaining_count = so.apply(rem)
                    discounted_value += special_offer_value
                    rem -= remaining_count
                    return discounted_value + remaining_count * self.price
        return self.price * count

    @classmethod
    def new(cls, line_item_id: str, price: int, special_offer_str: str = None):
        discounts = new_special_offers(line_item_id, special_offer_str or "")
        discounts.sort(key=lambda x: x.multiple, reverse=True)
        return cls(
            price=price,
            discounts=discounts,
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
            "A": LineItemData.new(
                "A", price=50, special_offer_str="3A for 130, 5A for 200"
            ),
            "B": LineItemData.new("B", price=30, special_offer_str="2B for 45"),
            "C": LineItemData.new("C", price=20),
            "D": LineItemData.new("D", price=15),
        }
    )


def compute_checkout_value(price_table: PriceTable, items: Dict[str, int]) -> int:
    checkout_value = 0
    for item, count in items.items():
        line_item = price_table.get_data_for(item)
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

    return compute_checkout_value(price_table, items_found)

