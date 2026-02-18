"""
Sudoku Solver using backtracking algorithm.
Solves any valid 9x9 Sudoku puzzle.
"""


def print_board(board):
    """Display the Sudoku board in a readable format."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        row = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                row += "| "
            row += str(board[i][j]) if board[i][j] != 0 else "."
            row += " "
        print(row)


def get_candidates(board, row, col):
    """Get the set of valid numbers for a cell."""
    used = set(board[row])
    used.update(board[i][col] for i in range(9))
    br, bc = 3 * (row // 3), 3 * (col // 3)
    used.update(board[br + r][bc + c] for r in range(3) for c in range(3))
    return set(range(1, 10)) - used


def find_empty(board):
    """Find the empty cell with fewest candidates (MRV heuristic). Returns (row, col) or None."""
    best, best_count = None, 10
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                count = len(get_candidates(board, i, j))
                if count < best_count:
                    best, best_count = (i, j), count
    return best


def is_valid(board, num, pos):
    """Check if placing num at pos (row, col) is valid."""
    row, col = pos

    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False

    return True


def solve(board):
    """Solve the Sudoku puzzle using backtracking. Returns True if solved."""
    empty = find_empty(board)
    if not empty:
        return True  # No empty cells = solved

    row, col = empty
    for num in get_candidates(board, row, col):
        board[row][col] = num
        if solve(board):
            return True
        board[row][col] = 0  # Backtrack

    return False


def is_valid_board(board):
    """Validate that the initial board state has no conflicts."""
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                num = board[i][j]
                board[i][j] = 0
                if not is_valid(board, num, (i, j)):
                    board[i][j] = num
                    return False
                board[i][j] = num
    return True


if __name__ == "__main__":
    # Example puzzle (0 = empty cell)
    puzzle = [
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

    print("Sudoku Puzzle:")
    print_board(puzzle)
    print()

    if not is_valid_board(puzzle):
        print("Invalid puzzle!")
    elif solve(puzzle):
        print("Solved:")
        print_board(puzzle)
    else:
        print("No solution exists.")
