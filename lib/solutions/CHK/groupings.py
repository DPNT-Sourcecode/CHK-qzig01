from typing import Dict


def compute_groupings_cost(items: Dict[str, int]):
    # pull out discounted items STXYZ
    to_look_for = ["Z", "Y", "X", "S", "T"]
    found_di = {}
    for di in to_look_for:
        if di in items:
            found_di[di] = items[di]
    count_ordered = []
    for tlf in to_look_for:
        if tlf in found_di:
            count_ordered.append((tlf, found_di[tlf]))
    if len(count_ordered) > 0:
        # while have at least 3 in list, pluck out
        last_entry = count_ordered[-1]
        total_entries = 0
        for i, n in count_ordered:
            total_entries += n
        print(total_entries, last_entry)
        if total_entries % 3 == 0:
            cost_of_groupings = int(total_entries / 3) * 45
        else:
            rem = total_entries % 3
            whole = int(total_entries / 3)
            remaining_item_id = last_entry[0]
            remaining_item_count = rem
            groupings_cost = whole * 45
    return groupings_cost, (remaining_item_id, remaining_item_count)
