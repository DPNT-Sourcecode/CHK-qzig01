from dataclasses import dataclass, field
from typing import Dict
from .line_item_data import LineItemData


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
