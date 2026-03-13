from connect4_core.disk import Disk


class TestInversion:
    def test_inversion_x_to_o(self):
        assert ~Disk.X == Disk.O

    def test_inversion_o_to_x(self):
        assert ~Disk.O == Disk.X
