from typing import Dict


def count_remainder(count_ordered):
    remaining_count = 0
    for item, count in count_ordered:
        remaining_count += count
    return remaining_count


def compute_groupings_cost(to_look_for, items: Dict[str, int]):
    # pull out discounted items STXYZ

    found_di = {}
    for di in to_look_for:
        if di in items:
            found_di[di] = items[di]
    if len(found_di) == 0:
        return 0, [("", 0)]
    count_ordered = []
    for tlf in to_look_for:
        if tlf in found_di:
            count_ordered.append((tlf, found_di[tlf]))

    s = ""
    for id, c in count_ordered:
        s += id * c

    print(count_ordered, count_remainder(count_ordered), s)
    if len(count_ordered) > 0:
        print(len(count_ordered))
        # while have at least 3 in list, pluck out
        last_entry = count_ordered[-1]
        total_entries = 0
        for i, n in count_ordered:
            total_entries += n
        if total_entries % 3 == 0:
            cost_of_groupings = int(total_entries / 3) * 45
            return cost_of_groupings, [("", 0)]
        else:
            rem = total_entries % 3
            whole = int(total_entries / 3)
            remaining_item_id = last_entry[0]
            remaining_item_count = rem
            groupings_cost = whole * 45
            return groupings_cost, [(remaining_item_id, remaining_item_count)]


