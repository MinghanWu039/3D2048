# 3D 2048: A New Dimension

A Python & Pygame Project

---

## What is 3D 2048?

- An evolution of the classic 2048 puzzle game.
- Extends the 2D grid into a third dimension.
- The game board is a **4x4x2** grid, composed of two stacked 4x4 layers.
- Introduces two new axes of movement: **Front** and **Back**.

---

## How to Play

- **Goal:** Merge matching tiles to create a tile with the number 2048.
- **Movement:**
  - **Planar:** Use `WASD` or `Arrow Keys` to move tiles Up, Down, Left, or Right on both layers simultaneously.
  - **Depth:** Use `Q` and `E` to move tiles Front (layer 2 -> layer 1) and Back (layer 1 -> layer 2).
- **Spawning:** A new tile (2 or 4) appears in a random empty cell after every successful move.

---

## Technical Deep Dive: Game Logic

### The "Backend": `Game3D2048` Class

- **Data Structure:** A 3D list (`list[list[list[int]]]`) represents the 4x4x2 grid.
- **Core Algorithm:** A single, elegant function `_move_and_merge_line` handles the sliding and merging logic for any 1D array of tiles.
- **Efficiency:** This core function is reused for all 6 movement directions by simply passing different "slices" of the 3D grid.

---

## Technical Deep Dive: The UI

### The "Frontend": `GameUI` Class with Pygame

- **Dual View:** The UI presents two distinct perspectives simultaneously:
  - **Two 2D Grids:** A clear, side-by-side representation of each layer, showing tile numbers.
  - **One 3D Visualization:** An interactive, rendered view of the entire game state.
- **UI Elements:**
  - Real-time score display.
  - Persistent on-screen key mapping instructions.
  - "Game Over" overlay.

---

## The 3D Visualization Engine

### Bringing it to Life in 3D

- **3D-to-2D Projection:**
  - Cube vertices are defined in 3D space.
  - They are mathematically **rotated** based on mouse input.
  - A **perspective projection** formula is applied to simulate depth, making farther objects appear smaller.
- **The Painter's Algorithm:**
  - To render solid, opaque cubes, we treat every face of every cube as a separate polygon.
  - Before drawing, we collect **all faces** from **all cubes** into a single list.
  - These faces are **sorted globally** based on their distance from the camera (far to near).
  - Finally, they are drawn in that sorted order, ensuring correct occlusion and a solid appearance.
- **Interactivity:** Mouse drag events update the horizontal rotation angle (`angle_y`), allowing for a stable, level view of the 3D grid.

---

## Feature Summary

- **Intuitive Dual View:** Combines the clarity of 2D with the immersion of 3D.
- **Solid 3D Rendering:** Robust painter's algorithm ensures correct visual representation from any angle.
- **Interactive Control:** Smooth horizontal rotation of the 3D view via mouse drag.
- **Flexible Inputs:** Supports both `WASD` and `Arrow Keys`.
- **Clear Player Guidance:** On-screen score and control instructions.

---

## Future Improvements

- **Animations:** Smoothly animate tile sliding and merging instead of instant updates.
- **Sound Effects:** Add audio feedback for moves and merges.
- **High Score System:** Implement saving and displaying high scores.
- **Configurable Grids:** Allow players to choose different grid sizes (e.g., 3x3x3).

---

## Questions?
