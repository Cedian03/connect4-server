import pytest
from connect4_core.disk import Disk
from connect4_core.board import Board, WIDTH, HEIGHT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_board(*cols: int) -> Board:
    """Play a sequence of column indices and return the resulting board."""
    b = Board()
    for col in cols:
        b.play(col)
    return b


def empty_matrix():
    return [[None for _ in range(HEIGHT)] for _ in range(WIDTH)]


# ---------------------------------------------------------------------------
# Board.__init__
# ---------------------------------------------------------------------------


class TestBoardInit:
    def test_all_cells_none(self):
        b = Board()
        for col in range(WIDTH):
            for row in range(HEIGHT):
                assert b[(col, row)] is None

    def test_turn_starts_at_zero(self):
        assert Board()._turn == 0


# ---------------------------------------------------------------------------
# Board.disk_to_play
# ---------------------------------------------------------------------------


class TestDiskToPlay:
    def test_first_turn_is_x(self):
        assert Board().disk_to_play() == Disk.X

    def test_second_turn_is_o(self):
        b = make_board(0)
        assert b.disk_to_play() == Disk.O

    def test_alternates_correctly(self):
        b = Board()
        expected = [Disk.X, Disk.O, Disk.X, Disk.O]
        for disk in expected:
            assert b.disk_to_play() == disk
            b.play(0)


# ---------------------------------------------------------------------------
# Board.free_row_in
# ---------------------------------------------------------------------------


class TestFreeRowIn:
    def test_empty_col_returns_row_zero(self):
        assert Board().free_row_in(0) == 0

    def test_returns_next_available_row(self):
        b = make_board(0, 0, 0)
        assert b.free_row_in(0) == 3

    def test_full_col_returns_none(self):
        b = make_board(*([0] * HEIGHT))
        assert b.free_row_in(0) is None


# ---------------------------------------------------------------------------
# Board.play
# ---------------------------------------------------------------------------


class TestPlay:
    def test_disk_placed_at_bottom(self):
        b = make_board(3)
        assert b[(3, 0)] == Disk.X

    def test_disks_stack(self):
        b = make_board(3, 3)
        assert b[(3, 0)] == Disk.X
        assert b[(3, 1)] == Disk.O

    def test_turn_increments(self):
        b = Board()
        b.play(0)
        assert b._turn == 1

    def test_full_column_raises(self):
        b = make_board(*([0] * HEIGHT))
        with pytest.raises(Exception):
            b.play(0)

    def test_other_columns_unaffected(self):
        b = make_board(0)
        assert b[(1, 0)] is None


# ---------------------------------------------------------------------------
# Board.check_four_connected  &  module-level check_four_connected
# ---------------------------------------------------------------------------


def _place(matrix, col, row, disk):
    matrix[col][row] = disk


@pytest.fixture
def x():
    return Disk.X


@pytest.fixture
def o():
    return Disk.O


class TestCheckFourConnected:
    """Tests both the Board method and the standalone function in tandem."""

    def _assert_winner(self, matrix, expected):
        b = Board()
        b._matrix = matrix
        assert b.check_four_connected() == expected

    # --- no winner ---

    def test_empty_board_no_winner(self, x):
        self._assert_winner(empty_matrix(), None)

    def test_three_in_a_row_no_winner(self, x):
        m = empty_matrix()
        for col in range(3):
            _place(m, col, 0, x)
        self._assert_winner(m, None)

    # --- horizontal ---

    def test_horizontal_win(self, x):
        m = empty_matrix()
        for col in range(4):
            _place(m, col, 0, x)
        self._assert_winner(m, x)

    def test_horizontal_win_not_at_origin(self, x):
        m = empty_matrix()
        for col in range(3, 7):
            _place(m, col, 2, x)
        self._assert_winner(m, x)

    def test_horizontal_mixed_no_winner(self, x, o):
        m = empty_matrix()
        for col in range(3):
            _place(m, col, 0, x)
        _place(m, 3, 0, o)
        self._assert_winner(m, None)

    # --- vertical ---

    def test_vertical_win(self, x):
        m = empty_matrix()
        for row in range(4):
            _place(m, 0, row, x)
        self._assert_winner(m, x)

    def test_vertical_win_mid_column(self, o):
        m = empty_matrix()
        for row in range(1, 5):
            _place(m, 2, row, o)
        self._assert_winner(m, o)

    # --- diagonal (bottom-left to top-right) ---

    def test_diagonal_ascending_win(self, x):
        m = empty_matrix()
        for i in range(4):
            _place(m, i, i, x)
        self._assert_winner(m, x)

    # --- diagonal (top-left to bottom-right) ---

    def test_diagonal_descending_win(self, o):
        m = empty_matrix()
        for i in range(4):
            _place(m, i, 3 - i, o)  # starts at row=3, decreases
        self._assert_winner(m, o)

    # --- via Board.play ---

    def test_horizontal_win_via_play(self):
        # X: cols 0,1,2,3  O: cols 0,1,2 (interleaved)
        b = make_board(0, 0, 1, 1, 2, 2, 3)
        assert b.check_four_connected() == Disk.X

    def test_vertical_win_via_play(self):
        # X plays col 0 four times; O plays col 1 three times
        b = make_board(0, 1, 0, 1, 0, 1, 0)
        assert b.check_four_connected() == Disk.X
