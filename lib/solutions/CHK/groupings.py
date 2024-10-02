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
        return 0, {}
    count_ordered = []
    for tlf in to_look_for:
        if tlf in found_di:
            count_ordered.append((tlf, found_di[tlf]))

    s = ""
    for id, c in count_ordered:
        s += id * c

    if len(count_ordered) > 0:
        print(len(s), len(s) % 3, int(len(s) / 3))
        rem_s = s[int(len(s) / 3) * 3 :]
        groupings_cost = int(len(s) / 3) * 45
        remaining_items = {c: rem_s.count(c) for c in rem_s}

        return groupings_cost, remaining_items
    return 0, {}




