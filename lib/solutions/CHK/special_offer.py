from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Discount:
    special_offer_str: str = ""
    offer_price: int = 0
    multiple: int = 0

    @property
    def has_offer(self):
        return self.offer_price != 0 and self.multiple != 0

    def apply(self, count: int) -> Tuple[int, int]:
        rem = count % self.multiple
        whole = int(count / self.multiple)
        return self.offer_price * whole, count - rem

    @classmethod
    def new(cls, line_item_id: str, sos: str):
        if sos == "":
            return cls()
        if line_item_id not in sos:
            raise Exception("invalid")
        tokens = sos.split(" for ")
        multiple = int(tokens[0].replace(line_item_id, ""))
        price = int(tokens[1])
        return cls(special_offer_str=sos, offer_price=price, multiple=multiple)


@dataclass
class BoGoF:
    multiple: int = 0
    subtract: int = 0
    free_item_id: str = ""
    min_needed: int = 0

    def apply(self, count) -> Tuple[int, str]:
        if self.subtract != 0:
            return self.apply_subtract(count)
        if count < self.min_needed:
            return 0, ""
        if count >= self.multiple:
            return int(count / self.multiple), self.free_item_id
        else:
            return 0, ""

    def apply_subtract(self, count):
        if count < self.min_needed:
            return 0, ""
        return self.subtract * int(count / self.min_needed), self.free_item_id


@dataclass
class GroupDiscount:
    number: int
    line_item_ids: List[str]
    price: int


def new_bogof(line_item_id: str, sos_str: str):
    if sos_str.count(line_item_id) == 2:
        min_needed = int(sos_str[0])
        return BoGoF(min_needed, 1, line_item_id, min_needed + 1)

    c = int(sos_str[0])
    tokens = sos_str.split("get one")[1].split("free")[0].strip()
    return BoGoF(c, 0, tokens, c)


def new_special_offers(
    line_item_id: str, sos_str: str
) -> Tuple[List[Discount], List[BoGoF], List[GroupDiscount]]:
    discounts: List[Discount] = []
    bogofs: List[BoGoF] = []
    group_discounts: List[GroupDiscount] = []
    if sos_str is None:
        return [], [], []
    if sos_str == "":
        return [], [], []
    if "buy any" in sos_str:
        return [], [], [GroupDiscount(3, ["S", "T", "X", "Y", "Z"], 45)]
    for so_str in sos_str.split(", "):
        if "for" in so_str:
            discounts.append(Discount.new(line_item_id, so_str))
        if "get one" in so_str:
            bogofs.append(new_bogof(line_item_id, sos_str=so_str))

    return discounts, bogofs, group_discounts



