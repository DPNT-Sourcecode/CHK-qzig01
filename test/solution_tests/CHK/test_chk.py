from lib.solutions.CHK.checkout_solution import (
    load_price_table,
    Discount,
    checkout,
    compute_checkout_value,
    LineItemData,
)


class TestComputeCheckoutValue:
    def test_one_of_each(self):
        price_table = load_price_table()
        items = {"A": 1, "B": 1, "C": 1, "D": 1}
        assert compute_checkout_value(price_table, items) == 115

    def test_trigger_special_offer_on_b(self):
        price_table = load_price_table()
        assert compute_checkout_value(price_table, {"B": 2}) == 45
        assert compute_checkout_value(price_table, {"B": 4}) == 90
        assert compute_checkout_value(price_table, {"B": 3}) == 45 + 30
        assert compute_checkout_value(price_table, {"B": 5}) == 90 + 30
        assert compute_checkout_value(price_table, {"A": 5}) == 200
        assert compute_checkout_value(price_table, {"A": 7}) == 200 + 2 * 50
        assert compute_checkout_value(price_table, {"A": 8}) == 200 + 130
        assert compute_checkout_value(price_table, {"A": 9}) == 200 + 130 + 50

    def test_trigger_bogof(self):
        price_table = load_price_table()
        assert compute_checkout_value(price_table, {"B": 1, "E": 2}) == 40 + 40

    def test_compute(self):
        price_table = load_price_table()

        assert compute_checkout_value(
            price_table, {"A": 3, "B": 2, "C": 3, "D": 1}
        ) == 130 + 45 + (3 * 20) + (1 * 15)


class TestChk:
    def test_load_price_table_ok(self):
        price_table = load_price_table()
        assert price_table.count_items == 6
        assert price_table.line_item_in_table("A")
        assert not price_table.line_item_in_table("AB")
        assert price_table.line_item_in_table("E")


class TestSpecialOffer:
    def test_parse_ok(self):
        input_so = "3A for 130"
        so = Discount.new("A", input_so)
        assert so.has_offer
        assert so.multiple == 3
        assert so.offer_price == 130

    def test_parse_ok_no_so(self):
        input_so = ""
        so = Discount.new("A", input_so)
        assert not so.has_offer


class TestMultipleDiscounts:
    def test_multiple(self):
        line_item = LineItemData.new(
            "A", price=50, special_offer_str="3A for 130, 5A for 200"
        )
        assert line_item.get_value(1) == 50
        assert line_item.get_value(2) == 2 * 50
        assert line_item.get_value(3) == 130
        assert line_item.get_value(4) == 130 + 50
        assert line_item.get_value(5) == 200
        assert line_item.get_value(6) == 200 + 50
        assert line_item.get_value(7) == 200 + 50 + 50
        assert line_item.get_value(8) == 200 + 130


class TestBogof:
    def test_with_bogof(self):
        line_item = LineItemData.new(
            "E", price=40, special_offer_str="2E get one B free"
        )
        assert line_item.has_bogofs

    def test_with_bogof(self):
        line_item = LineItemData.new(
            "E", price=40, special_offer_str="2E get one B free"
        )
        assert 2, "B" == line_item.get_freebies(4)
        assert 2, "B" == line_item.get_freebies(5)
        assert 3, "B" == line_item.get_freebies(6)


class TestCheckout:
    def test_checkout_invalid_sku(self):
        assert checkout("ABG") == -1

    def test_one(self):
        assert checkout("A") == 50

    def test_many(self):
        assert checkout("AAABBCCCD") == 130 + 45 + (3 * 20) + (1 * 15)

    def test_many_random_order(self):
        assert checkout("ABABCACCD") == 130 + 45 + (3 * 20) + (1 * 15)

    def test_many_with_bogof(self):
        assert checkout("AAABBCCCDEE") == 130 + 30 + (3 * 20) + (1 * 15) + (2 * 40)

    def test_e(self):
        assert checkout("E") == 40

    def test_ABCDE(self):
        assert checkout("ABCDE") == 155

    def test_AAAAA(self):
        assert checkout("AAAAA") == 200


class TestF:
    def test_has_F(self):
        price_table = load_price_table()
        assert price_table.line_item_in_table("F")

