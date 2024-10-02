from lib.solutions.CHK.checkout_solution import load_price_table, SpecialOffer


class TestChk:
    def test_load_price_table_ok(self):
        table = load_price_table()
        assert table.count_items == 4
        assert table.line_item_in_table("A")
        assert not table.line_item_in_table("AB")


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

