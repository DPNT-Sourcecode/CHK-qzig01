from typing import Dict, List
from .price_table import PriceTable, load_price_table


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
