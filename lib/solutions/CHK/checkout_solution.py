from typing import Dict, List
from .price_table import PriceTable, load_price_table
from .groupings import compute_groupings_cost


def compute_checkout_value(price_table: PriceTable, items: Dict[str, int]) -> int:

    checkout_value_per_item = {}
    # s20 T20 X17 Y20 Z21
    # ZYTSX
    to_look_for = ["Z", "Y", "S", "T", "X"]
    groupings_cost, remaining_items = compute_groupings_cost(to_look_for, items, 3, 45)
    for tlf in to_look_for:
        if tlf in items:
            del items[tlf]

    for remain_id, remain_count in remaining_items.items():
        if remain_id != "":
            items[remain_id] = remain_count

    free_items = {}
    for item, count in items.items():
        line_item = price_table.get_data_for(item)
        free_item_count, free_item = line_item.get_freebies(count)

        if free_item == "":
            continue
        if free_item not in free_items:
            free_items[free_item] = 0
        free_items[free_item] += free_item_count

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

    return total + groupings_cost


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



