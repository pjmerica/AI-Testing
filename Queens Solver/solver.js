/**
 * Queens Puzzle Solver
 * Rules:
 *  - N×N grid with N color regions
 *  - Place exactly one queen per row, per column, and per region
 *  - No two queens may touch (including diagonally)
 */

function solve(colorGrid) {
  const N = colorGrid.length;
  const queens = []; // queens[row] = col
  const usedCols = new Set();
  const usedRegions = new Set();

  function adjacent(r1, c1, r2, c2) {
    return Math.abs(r1 - r2) <= 1 && Math.abs(c1 - c2) <= 1;
  }

  function conflicts(row, col) {
    for (const [qr, qc] of queens) {
      if (adjacent(qr, qc, row, col)) return true;
    }
    return false;
  }

  function backtrack(row) {
    if (row === N) return queens.length === N;

    for (let col = 0; col < N; col++) {
      if (usedCols.has(col)) continue;
      const region = colorGrid[row][col];
      if (usedRegions.has(region)) continue;
      if (conflicts(row, col)) continue;

      queens.push([row, col]);
      usedCols.add(col);
      usedRegions.add(region);

      if (backtrack(row + 1)) return true;

      queens.pop();
      usedCols.delete(col);
      usedRegions.delete(region);
    }
    return false;
  }

  if (backtrack(0)) return queens;
  return null;
}

// Export for use in Node or as a module
if (typeof module !== "undefined") module.exports = { solve };
