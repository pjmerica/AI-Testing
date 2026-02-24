/**
 * LinkedIn Queens Auto-Solver
 * Run this as a bookmarklet on linkedin.com/games/queens
 *
 * Strategy: Try multiple DOM detection approaches since LinkedIn may change their markup.
 */

(function () {
  // ─── SOLVER ──────────────────────────────────────────────────────────────────

  function solve(colorGrid) {
    const N = colorGrid.length;
    const queens = [];
    const usedCols = new Set();
    const usedRegions = new Set();

    function conflicts(row, col) {
      for (const [qr, qc] of queens) {
        if (Math.abs(qr - row) <= 1 && Math.abs(qc - col) <= 1) return true;
      }
      return false;
    }

    function backtrack(row) {
      if (row === N) return true;
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

    return backtrack(0) ? queens : null;
  }

  // ─── DOM DETECTION ───────────────────────────────────────────────────────────

  function rgbToKey(rgb) {
    // Normalise an rgb/rgba string to a stable colour key
    return rgb.replace(/\s/g, "").toLowerCase();
  }

  function detectBoard() {
    // --- Attempt 1: data-cell-coordinate attributes (seen in some builds) ---
    {
      const cells = document.querySelectorAll("[data-cell-coordinate]");
      if (cells.length > 0) {
        let maxRow = 0, maxCol = 0;
        const raw = [];
        cells.forEach(cell => {
          const coord = cell.getAttribute("data-cell-coordinate").split(",");
          const r = parseInt(coord[0]), c = parseInt(coord[1]);
          maxRow = Math.max(maxRow, r);
          maxCol = Math.max(maxCol, c);
          raw.push({ r, c, el: cell });
        });
        const N = maxRow + 1;
        if (Math.sqrt(raw.length) === N || raw.length === N * N) {
          return buildGrid(raw, N);
        }
      }
    }

    // --- Attempt 2: aria-label like "Row 1, Column 1" ---
    {
      const cells = [...document.querySelectorAll("[aria-label]")].filter(el =>
        /row\s*\d+.*col(umn)?\s*\d+/i.test(el.getAttribute("aria-label"))
      );
      if (cells.length > 1) {
        const raw = cells.map(el => {
          const m = el.getAttribute("aria-label").match(/row\s*(\d+).*col(?:umn)?\s*(\d+)/i);
          return { r: parseInt(m[1]) - 1, c: parseInt(m[2]) - 1, el };
        });
        const N = Math.max(...raw.map(x => x.r)) + 1;
        if (raw.length === N * N) return buildGrid(raw, N);
      }
    }

    // --- Attempt 3: CSS grid children with background-color ---
    {
      const candidates = [
        ".queens-game-board",
        ".game-board",
        '[class*="queens"]',
        '[class*="game-board"]',
        '[class*="board"]',
      ];
      for (const sel of candidates) {
        const board = document.querySelector(sel);
        if (!board) continue;
        const cells = [...board.querySelectorAll("*")].filter(el => {
          const s = window.getComputedStyle(el);
          const bg = s.backgroundColor;
          return (
            bg && bg !== "rgba(0, 0, 0, 0)" && bg !== "transparent" &&
            el.children.length === 0 || el.querySelector("button,div,span") !== null
          );
        });
        // Try to find clickable leaf cells
        const clickable = [...board.querySelectorAll("button, [role='button'], [tabindex]")]
          .filter(el => el.closest(sel) === board || board.contains(el));
        if (clickable.length >= 4) {
          const N = Math.round(Math.sqrt(clickable.length));
          if (N * N === clickable.length) {
            const raw = clickable.map((el, i) => ({
              r: Math.floor(i / N), c: i % N, el
            }));
            return buildGrid(raw, N);
          }
        }
      }
    }

    // --- Attempt 4: find any NxN grid of same-tag siblings with colour ---
    {
      const allDivs = document.querySelectorAll("div, td, li");
      for (const container of allDivs) {
        const kids = [...container.children].filter(
          el => ["DIV", "TD", "LI", "BUTTON"].includes(el.tagName)
        );
        const N = Math.round(Math.sqrt(kids.length));
        if (N >= 4 && N * N === kids.length) {
          const colorSet = new Set(
            kids.map(el => rgbToKey(window.getComputedStyle(el).backgroundColor))
              .filter(c => c !== "rgba(0,0,0,0)" && c !== "transparent")
          );
          if (colorSet.size >= Math.max(N - 2, 2)) {
            const raw = kids.map((el, i) => ({ r: Math.floor(i / N), c: i % N, el }));
            return buildGrid(raw, N);
          }
        }
      }
    }

    return null;
  }

  function buildGrid(raw, N) {
    // Assign region IDs based on background colour
    const colorMap = new Map();
    let nextId = 0;

    const grid = Array.from({ length: N }, () => Array(N).fill(0));
    const cellEls = Array.from({ length: N }, () => Array(N).fill(null));

    raw.forEach(({ r, c, el }) => {
      // Walk up to find first element with a non-transparent background
      let colorEl = el;
      let bg = "";
      for (let depth = 0; depth < 5; depth++) {
        bg = window.getComputedStyle(colorEl).backgroundColor;
        if (bg && bg !== "rgba(0, 0, 0, 0)" && bg !== "transparent") break;
        if (!colorEl.parentElement) break;
        colorEl = colorEl.parentElement;
      }
      const key = rgbToKey(bg) || `pos-${r}-${c}`;
      if (!colorMap.has(key)) colorMap.set(key, nextId++);
      grid[r][c] = colorMap.get(key);
      cellEls[r][c] = el;
    });

    return { grid, cellEls, N };
  }

  // ─── CLICK HELPERS ───────────────────────────────────────────────────────────

  function clickCell(el) {
    // Some LinkedIn games need two clicks (first = X mark, second = queen)
    // Try dispatching pointer + mouse + click events
    ["pointerdown", "mousedown", "click", "pointerup", "mouseup"].forEach(type => {
      el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true }));
    });
  }

  async function placeQueens(queens, cellEls, doubleClick) {
    for (const [row, col] of queens) {
      const el = cellEls[row][col];
      if (!el) { console.warn(`No element at [${row},${col}]`); continue; }

      clickCell(el);
      if (doubleClick) {
        await delay(120);
        clickCell(el);
      }
      await delay(200);
    }
  }

  function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

  // ─── OVERLAY UI ──────────────────────────────────────────────────────────────

  function showOverlay(message, color = "#10b981") {
    let overlay = document.getElementById("__queens_solver_overlay");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.id = "__queens_solver_overlay";
      Object.assign(overlay.style, {
        position: "fixed", top: "20px", right: "20px", zIndex: "999999",
        padding: "14px 20px", borderRadius: "10px", fontFamily: "system-ui, sans-serif",
        fontSize: "14px", fontWeight: "600", color: "#fff",
        boxShadow: "0 4px 20px rgba(0,0,0,0.3)", maxWidth: "320px",
        transition: "background 0.3s",
      });
      document.body.appendChild(overlay);
    }
    overlay.style.background = color;
    overlay.textContent = message;
    setTimeout(() => overlay.remove(), 5000);
  }

  // ─── MAIN ────────────────────────────────────────────────────────────────────

  async function main() {
    showOverlay("Queens Solver: detecting board...", "#6366f1");

    const result = detectBoard();
    if (!result) {
      showOverlay("❌ Could not detect the game board. Make sure you're on the Queens game page.", "#ef4444");
      console.error("[Queens Solver] Board detection failed. Dumping page for debug:", document.body.innerHTML.slice(0, 2000));
      return;
    }

    const { grid, cellEls, N } = result;
    console.log("[Queens Solver] Detected grid:", grid);

    const regions = new Set(grid.flat());
    if (regions.size !== N) {
      showOverlay(`⚠️ Detected ${N}×${N} grid but only ${regions.size} colour regions (expected ${N}). Trying anyway...`, "#f59e0b");
    }

    const solution = solve(grid);
    if (!solution) {
      showOverlay("❌ No solution found. The board may not have been read correctly.", "#ef4444");
      return;
    }

    console.log("[Queens Solver] Solution:", solution);
    showOverlay(`✅ Solved! Placing ${solution.length} queens...`, "#10b981");

    // Try single-click first; if LinkedIn uses toggle (X → queen), use doubleClick
    await placeQueens(solution, cellEls, false);
    showOverlay("✅ Done! Queens placed.", "#10b981");
  }

  main().catch(err => {
    console.error("[Queens Solver]", err);
    showOverlay("❌ Error: " + err.message, "#ef4444");
  });
})();
