from lib.solutions.CHK.checkout_solution import load_price_table


class TestChk:
    def test_load_price_table_ok(self):
        table = load_price_table()
        assert table.count_items == 4


