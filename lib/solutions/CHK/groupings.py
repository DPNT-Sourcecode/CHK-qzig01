from typing import Dict, List


def compute_groupings_cost(
    to_look_for: List[str], items: Dict[str, int], group_size: int, group_cost: int
):
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
    print(s, count_ordered)
    if len(count_ordered) > 0:
        rem_s = s[int(len(s) / group_size) * group_size :]
        groupings_cost = int(len(s) / group_size) * group_cost
        remaining_items = {c: rem_s.count(c) for c in rem_s}

        return groupings_cost, remaining_items
    return 0, {}






