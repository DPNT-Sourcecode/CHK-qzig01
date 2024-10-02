from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class SelfMultipleSpecialOffer:
    special_offer_str: str = ""
    offer_price: int = 0
    multiple: int = 0

    @property
    def has_offer(self):
        return self.offer_price != 0 and self.multiple != 0

    def apply(self, count: int, price: int) -> int:
        rem = count % self.multiple
        whole = int(count / self.multiple)
        return self.offer_price * whole + rem * price

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


def new_special_offer(line_item_id: str, so_str: str) -> SelfMultipleSpecialOffer:
    if "for" in so_str:
        return SelfMultipleSpecialOffer.new(line_item_id, so_str)
    if " get one " in so_str:
        raise NotImplementedError

    raise NotImplementedError


def new_special_offers(
    line_item_id: str, sos_str: str
) -> List[SelfMultipleSpecialOffer]:
    if sos_str is None:
        return []
    if sos_str == "":
        return []
    return [new_special_offer(line_item_id, so_str) for so_str in sos_str.split(", ")]
