from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from lib.solutions.CHK.special_offer import Discount, new_special_offers, BoGoF


@dataclass
class LineItemData:

    price: int
    discounts: List[Discount] = field(default_factory=list)
    bogofs: List[BoGoF] = field(default_factory=list)

    @property
    def has_discounts(self) -> bool:
        return len(self.discounts) > 0

    @property
    def has_bogofs(self) -> bool:
        return len(self.bogofs) > 0

    def get_value(self, count: int):
        if self.has_discounts:
            discounted_value = 0
            rem = count
            for discount in self.discounts:
                if rem >= discount.multiple:
                    special_offer_value, remaining_count = discount.apply(rem)
                    discounted_value += special_offer_value
                    rem -= remaining_count
            return discounted_value + rem * self.price
        return self.price * count

    def get_freebies(self, count: int) -> Tuple[int, str]:
        if not self.has_bogofs:
            return 0, ""
        count_free, free_item_id = self.bogofs[0].apply(count)
        print(count_free, self.bogofs[0].min_needed)
        return count_free, free_item_id

    @classmethod
    def new(cls, line_item_id: str, price: int, special_offer_str: str = None):
        discounts, bogofs = new_special_offers(line_item_id, special_offer_str or "")
        discounts.sort(key=lambda x: x.multiple, reverse=True)
        return cls(price=price, discounts=discounts, bogofs=bogofs)


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
            "E": LineItemData.new("E", price=40, special_offer_str="2E get one B free"),
            "F": LineItemData.new("F", price=10, special_offer_str="2F get one F free"),
        }
    )


def compute_checkout_value(price_table: PriceTable, items: Dict[str, int]) -> int:

    checkout_value_per_item = {}
    free_items = {}

    # compute bogofs
    for item, count in items.items():
        line_item = price_table.get_data_for(item)
        free_item_count, free_item = line_item.get_freebies(count)
        if free_item == "":
            continue
        if free_item not in free_items:
            free_items[free_item] = 0
        free_items[free_item] += free_item_count
    print("free_items", free_items)
    for item, count in items.items():
        if item in free_items:
            count = count - free_items[item]
        line_item = price_table.get_data_for(item)
        if item not in checkout_value_per_item:
            checkout_value_per_item[item] = 0
        checkout_value_per_item[item] += line_item.get_value(count)

    total = 0
    for _, value in checkout_value_per_item.items():
        total += value

    return total


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
