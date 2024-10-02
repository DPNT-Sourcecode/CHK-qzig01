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
    free_item_id: str = ""

    def apply(self, count) -> Tuple[int, str]:
        if count >= self.multiple:
            return int(count / self.multiple), self.free_item_id
        else:
            return 0, ""


def new_special_offers(
    line_item_id: str, sos_str: str
) -> Tuple[List[Discount], List[BoGoF]]:
    discounts: List[Discount] = []
    bogofs: List[BoGoF] = []
    if sos_str is None:
        return [], []
    if sos_str == "":
        return [], []
    for so_str in sos_str.split(", "):
        if "for" in so_str:
            discounts.append(Discount.new(line_item_id, so_str))
        if "2E get one B free" in so_str:
            bogofs.append(BoGoF(2, "B"))
        if "2F get one F free" in so_str:
            bogofs.append(BoGoF(2, "F"))

    return discounts, bogofs



