import json
from typing import Dict, List, Tuple, Optional


class Maze:
    def __init__(self, filename):
        self.filename = filename
        self.width: int = 0
        self.height: int = 0
        self.start: Tuple[int, int] = (0, 0)
        self.end: Tuple[int, int] = (0, 0)
        self.grid: List[List[Dict[str, bool]]] = []
        self.load_maze()

    def load_maze(self):
        with open(self.filename, "r") as f:
            data = json.load(f)

        size = data.get("size")
        if not size or len(size) != 2:
            raise ValueError("Maze JSON must include 'size': [width, height]")
        self.width, self.height = int(size[0]), int(size[1])

        start = data.get("start")
        if not start or len(start) != 2:
            raise ValueError("Maze JSON must include 'start': [x, y]")
        self.start = (int(start[0]), int(start[1]))

        end = data.get("end")
        if not end or len(end) != 2:
            raise ValueError("Maze JSON must include 'end': [x, y]")
        self.end = (int(end[0]), int(end[1]))

        # Grid is optional; if provided, should be height rows of width cells
        grid = data.get("maze") or []
        # Normalize grid to 2D list of dicts with wall flags
        self.grid = [[self._normalize_cell(grid, x, y) for x in range(self.width)] for y in range(self.height)]

    def _normalize_cell(self, grid: List[List[Dict[str, bool]]], x: int, y: int) -> Dict[str, bool]:
        # Default: no walls; you can move freely unless at boundary
        default_cell = {"up": False, "down": False, "left": False, "right": False}
        try:
            if y < len(grid) and x < len(grid[y]):
                raw = grid[y][x]
                if isinstance(raw, dict):
                    cell = {**default_cell}
                    for k in default_cell.keys():
                        if k in raw:
                            cell[k] = bool(raw[k])
                    return cell
        except Exception:
            pass
        return default_cell

    def is_within_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def can_move(self, from_pos: Tuple[int, int], direction: str) -> Tuple[bool, Optional[Tuple[int, int]], str]:
        x, y = from_pos
        if not self.is_within_bounds(x, y):
            return False, None, "Current position is out of bounds"

        dx, dy = 0, 0
        if direction == "up":
            dy = -1
        elif direction == "down":
            dy = 1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        else:
            return False, None, "Invalid direction"

        cell = self.grid[y][x]
        # Blocked if wall on exiting side
        if (direction == "up" and cell.get("up")) or \
           (direction == "down" and cell.get("down")) or \
           (direction == "left" and cell.get("left")) or \
           (direction == "right" and cell.get("right")):
            return False, None, "Blocked by wall"

        nx, ny = x + dx, y + dy
        if not self.is_within_bounds(nx, ny):
            return False, None, "Move would go out of bounds"

        # Also respect wall from neighbor's opposite side, if provided
        neighbor = self.grid[ny][nx]
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if neighbor.get(opposite[direction]):
            return False, None, "Blocked by neighboring wall"

        return True, (nx, ny), "Move allowed"

    def is_at_end(self, pos: Tuple[int, int]) -> bool:
        return tuple(pos) == tuple(self.end)

    def render_ascii(self, robot_pos: Optional[Tuple[int, int]] = None) -> str:
        lines: List[str] = []
        # For each row, draw top walls, then cell row with vertical walls
        for y in range(self.height):
            # Top wall line for row y
            top_parts: List[str] = ["+"]
            for x in range(self.width):
                cell = self.grid[y][x]
                top_parts.append("---" if cell.get("up") else "   ")
                top_parts.append("+")
            lines.append("".join(top_parts))

            # Middle line with vertical walls and cell content
            mid_parts: List[str] = []
            # Emit the left boundary once using the first cell's left wall
            first_cell = self.grid[y][0]
            left_boundary = "|" if first_cell.get("left") else " "
            mid_parts.append(left_boundary)
            for x in range(self.width):
                cell = self.grid[y][x]
                # Determine content priority: Robot > Start > End > space
                content_char = " "
                if robot_pos is not None and (x, y) == tuple(robot_pos):
                    content_char = "R"
                elif (x, y) == tuple(self.start):
                    content_char = "S"
                elif (x, y) == tuple(self.end):
                    content_char = "E"
                mid_parts.append(f" {content_char} ")
                # Emit this cell's right wall as the separator to the next cell
                right_wall = "|" if cell.get("right") else " "
                mid_parts.append(right_wall)
            lines.append("".join(mid_parts))

        # Bottom wall line using last row's down walls
        bottom_parts: List[str] = ["+"]
        last_y = self.height - 1
        for x in range(self.width):
            cell = self.grid[last_y][x]
            bottom_parts.append("---" if cell.get("down") else "   ")
            bottom_parts.append("+")
        lines.append("".join(bottom_parts))

        return "\n".join(lines)

    def display_maze(self):
        for row in self.grid:
            for cell in row:
                print(cell)
            print()
