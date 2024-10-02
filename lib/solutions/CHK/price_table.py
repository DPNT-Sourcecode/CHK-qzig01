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
            "G": LineItemData.new("G", price=20),
            "H": LineItemData.new(
                "H", price=10, special_offer_str="5H for 45, 10H for 80"
            ),
            "I": LineItemData.new("I", price=35),
            "J": LineItemData.new("J", price=60),
            "K": LineItemData.new("K", price=80, special_offer_str="2K for 150"),
            "L": LineItemData.new("L", price=90),
            "M": LineItemData.new("M", price=15),
            "N": LineItemData.new("N", price=40, special_offer_str="3N get one M free"),
            "O": LineItemData.new("O", price=10),
        }
    )


def load_from_pipe_sep() -> PriceTable:
    pt = PriceTable()

    pipe_sep_str = """
    | A    | 50    | 3A for 130, 5A for 200 |
    | B    | 30    | 2B for 45              |
    | C    | 20    |                        |
    | D    | 15    |                        |
    | E    | 40    | 2E get one B free      |
    | F    | 10    | 2F get one F free      |
    | G    | 20    |                        |
    | H    | 10    | 5H for 45, 10H for 80  |
    | I    | 35    |                        |
    | J    | 60    |                        |
    | K    | 80    | 2K for 150             |
    | L    | 90    |                        |
    | M    | 15    |                        |
    | N    | 40    | 3N get one M free      |
    | O    | 10    |                        |
    | P    | 50    | 5P for 200             |
    | Q    | 30    | 3Q for 80              |
    | R    | 50    | 3R get one Q free      |
    | S    | 30    |                        |
    | T    | 20    |                        |
    | U    | 40    | 3U get one U free      |
    | V    | 50    | 2V for 90, 3V for 130  |
    | W    | 20    |                        |
    | X    | 90    |                        |
    | Y    | 10    |                        |
    | Z    | 50    |                        |"""

    tokens = pipe_sep_str.split("\n")
    print(tokens)

    return pt


