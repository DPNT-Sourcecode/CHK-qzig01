from lib.solutions.CHK.price_table import load_from_pipe_sep


class TestLoad:
    def test_load_ok(self):
        pt = load_from_pipe_sep()
        assert pt.count_items == 26
