from dataclasses import dataclass, field
from typing import List, Tuple
from .special_offer import Discount, new_special_offers, BoGoF, GroupDiscount


@dataclass
class LineItemData:

    price: int
    discounts: List[Discount] = field(default_factory=list)
    bogofs: List[BoGoF] = field(default_factory=list)
    group_discounts: List[GroupDiscount] = field(default_factory=list)

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
        return self.bogofs[0].apply(count)

    def get_group_discounts(self):
        if len(self.group_discounts) == 0:
            return None
        return self.group_discounts[0]

    @classmethod
    def new(cls, line_item_id: str, price: int, special_offer_str: str = None):
        discounts, bogofs, group_discounts = new_special_offers(
            line_item_id, special_offer_str or ""
        )
        discounts.sort(key=lambda x: x.multiple, reverse=True)
        return cls(
            price=price,
            discounts=discounts,
            bogofs=bogofs,
            group_discounts=group_discounts,
        )
