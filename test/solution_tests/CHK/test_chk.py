from lib.solutions.CHK.checkout_solution import (
    load_price_table,
    SpecialOffer,
    checkout,
    compute_checkout_value,
)


class TestComputeCheckoutValue:
    def test_one_of_each(self):
        price_table = load_price_table()
        items = {"A": 1, "B": 1, "C": 1, "D": 1}
        assert compute_checkout_value(price_table, items) == 115


class TestCheckout:
    def test_checkout_invalid_sku(self):
        assert checkout("ABF") == -1

    def test_one(self):
        assert checkout("A") == 50


class TestChk:
    def test_load_price_table_ok(self):
        price_table = load_price_table()
        assert price_table.count_items == 4
        assert price_table.line_item_in_table("A")
        assert not price_table.line_item_in_table("AB")


class TestSpecialOffer:
    def test_parse_ok(self):
        input_so = "3A for 130"
        so = SpecialOffer.new("A", input_so)
        assert so.has_offer
        assert so.multiple == 3
        assert so.price == 130

    def test_parse_ok_no_so(self):
        input_so = ""
        so = SpecialOffer.new("A", input_so)
        assert not so.has_offer



