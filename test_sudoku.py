"""Tests for the Sudoku solver."""
import copy
from sudoku_solver import solve, is_valid, find_empty, is_valid_board, get_candidates


# Known puzzle and its solution
PUZZLE = [
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

EXPECTED_SOLUTION = [
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


def check_solution_valid(board):
    """Verify every row, column, and 3x3 box contains 1-9 exactly once."""
    for i in range(9):
        if sorted(board[i]) != list(range(1, 10)):
            return False
        if sorted(board[j][i] for j in range(9)) != list(range(1, 10)):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            box = [board[br + r][bc + c] for r in range(3) for c in range(3)]
            if sorted(box) != list(range(1, 10)):
                return False
    return True


def test_solve_known_puzzle():
    """Test solving a well-known puzzle matches the expected solution."""
    board = copy.deepcopy(PUZZLE)
    assert solve(board)
    assert board == EXPECTED_SOLUTION


def test_solution_is_valid():
    """Test that the solution satisfies all Sudoku constraints."""
    board = copy.deepcopy(PUZZLE)
    solve(board)
    assert check_solution_valid(board)


def test_find_empty():
    """Test that find_empty correctly locates empty cells."""
    board = copy.deepcopy(PUZZLE)
    result = find_empty(board)
    assert result is not None
    assert board[result[0]][result[1]] == 0  # Must be an empty cell
    assert find_empty(EXPECTED_SOLUTION) is None  # No empties in solution


def test_is_valid():
    """Test move validation."""
    board = copy.deepcopy(PUZZLE)
    assert is_valid(board, 4, (0, 2))  # Valid placement
    assert not is_valid(board, 5, (0, 2))  # 5 already in row
    assert not is_valid(board, 9, (0, 2))  # 9 already in column
    assert not is_valid(board, 3, (0, 2))  # 3 already in 3x3 box


def test_is_valid_board():
    """Test board validation."""
    assert is_valid_board(copy.deepcopy(PUZZLE))
    # Board with duplicate in row
    bad_board = copy.deepcopy(PUZZLE)
    bad_board[0][2] = 5  # Duplicate 5 in row 0
    assert not is_valid_board(bad_board)


def test_hard_puzzle():
    """Test solving a harder puzzle."""
    hard = [
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
    assert solve(hard)
    assert check_solution_valid(hard)


def test_already_solved():
    """Test that a completed board is recognized as solved."""
    board = copy.deepcopy(EXPECTED_SOLUTION)
    assert solve(board)
    assert board == EXPECTED_SOLUTION


if __name__ == "__main__":
    tests = [
        test_solve_known_puzzle,
        test_solution_is_valid,
        test_find_empty,
        test_is_valid,
        test_is_valid_board,
        test_hard_puzzle,
        test_already_solved,
    ]
    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
        except AssertionError as e:
            print(f"FAIL: {test.__name__} - {e}")
    print(f"\nAll {len(tests)} tests completed.")
