"""Tests for the Sudoku solver."""

import copy
import unittest

from sudoku_solver import find_empty, get_candidates, is_valid, is_valid_board, solve


class TestSudokuSolver(unittest.TestCase):

    def setUp(self):
        self.easy_puzzle = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

        self.easy_solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]

        # Hard puzzle (requires more backtracking)
        self.hard_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 8, 5],
            [0, 0, 1, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 7, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 1, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 7, 3],
            [0, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 4, 0, 0, 0, 9],
        ]

        # Minimal puzzle (17 clues — fewest possible for a unique solution)
        self.minimal_puzzle = [
            [0, 0, 0, 0, 0, 0, 0, 1, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 4, 0, 7],
            [0, 0, 8, 0, 0, 0, 3, 0, 0],
            [0, 0, 1, 0, 9, 0, 0, 0, 0],
            [3, 0, 0, 4, 0, 0, 2, 0, 0],
            [0, 5, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 0, 6, 0, 0, 0],
        ]

    # --- solve() tests ---

    def test_solve_easy_puzzle(self):
        board = copy.deepcopy(self.easy_puzzle)
        self.assertTrue(solve(board))
        self.assertEqual(board, self.easy_solution)

    def test_solve_hard_puzzle(self):
        board = copy.deepcopy(self.hard_puzzle)
        self.assertTrue(solve(board))
        self._assert_valid_solution(board)

    def test_solve_minimal_puzzle(self):
        board = copy.deepcopy(self.minimal_puzzle)
        self.assertTrue(solve(board))
        self._assert_valid_solution(board)

    def test_solve_already_solved(self):
        board = copy.deepcopy(self.easy_solution)
        self.assertTrue(solve(board))
        self.assertEqual(board, self.easy_solution)

    def test_solve_unsolvable_puzzle(self):
        board = copy.deepcopy(self.easy_puzzle)
        # Place conflicting numbers to make it unsolvable
        board[0][0] = 1  # conflicts with row (already has 1 in solution context)
        board[0][1] = 2  # force more conflicts
        board[0][2] = 6
        board[1][1] = 4
        self.assertFalse(solve(board))

    def test_solve_empty_board(self):
        board = [[0] * 9 for _ in range(9)]
        self.assertTrue(solve(board))
        self._assert_valid_solution(board)

    # --- is_valid() tests ---

    def test_is_valid_row_conflict(self):
        board = copy.deepcopy(self.easy_puzzle)
        self.assertFalse(is_valid(board, 5, (0, 2)))  # 5 already in row 0

    def test_is_valid_col_conflict(self):
        board = copy.deepcopy(self.easy_puzzle)
        self.assertFalse(is_valid(board, 8, (0, 2)))  # 8 in column 2

    def test_is_valid_box_conflict(self):
        board = copy.deepcopy(self.easy_puzzle)
        self.assertFalse(is_valid(board, 9, (0, 2)))  # 9 in top-left box

    def test_is_valid_valid_placement(self):
        board = copy.deepcopy(self.easy_puzzle)
        self.assertTrue(is_valid(board, 4, (0, 2)))  # 4 is valid at (0,2)

    # --- is_valid_board() tests ---

    def test_valid_board(self):
        self.assertTrue(is_valid_board(self.easy_puzzle))

    def test_invalid_board_duplicate_in_row(self):
        board = copy.deepcopy(self.easy_puzzle)
        board[0][2] = 5  # duplicate 5 in row 0
        self.assertFalse(is_valid_board(board))

    def test_invalid_board_duplicate_in_col(self):
        board = copy.deepcopy(self.easy_puzzle)
        board[2][0] = 6  # duplicate 6 in column 0
        self.assertFalse(is_valid_board(board))

    def test_invalid_board_duplicate_in_box(self):
        board = copy.deepcopy(self.easy_puzzle)
        board[1][1] = 8  # duplicate 8 in top-left box
        self.assertFalse(is_valid_board(board))

    # --- get_candidates() tests ---

    def test_get_candidates(self):
        candidates = get_candidates(self.easy_puzzle, 0, 2)
        self.assertEqual(candidates, {1, 2, 4})

    def test_get_candidates_filled_cell(self):
        candidates = get_candidates(self.easy_puzzle, 0, 0)
        # Cell has 5; candidates exclude values already in row/col/box
        self.assertNotIn(5, candidates)

    # --- find_empty() tests ---

    def test_find_empty_returns_cell(self):
        result = find_empty(self.easy_puzzle)
        self.assertIsNotNone(result)
        row, col = result
        self.assertEqual(self.easy_puzzle[row][col], 0)

    def test_find_empty_solved_board(self):
        self.assertIsNone(find_empty(self.easy_solution))

    # --- helper ---

    def _assert_valid_solution(self, board):
        """Verify every row, column, and box contains 1-9 exactly once."""
        full = set(range(1, 10))
        for i in range(9):
            self.assertEqual(set(board[i]), full, f"Row {i} invalid")
            self.assertEqual(set(board[r][i] for r in range(9)), full, f"Col {i} invalid")
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box = {board[br + r][bc + c] for r in range(3) for c in range(3)}
                self.assertEqual(box, full, f"Box ({br},{bc}) invalid")


if __name__ == "__main__":
    unittest.main()
