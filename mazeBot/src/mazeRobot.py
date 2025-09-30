from typing import Tuple, List


class MazeRobot:
    def __init__(self):
        self.name = "MazeRobot"
        self.description = "A robot that navigates a maze"
        self.position = (0, 0)
        self.maze = None

    def move(self, direction) -> Tuple[bool, str]:
        if self.maze is None:
            return False, "Maze not set"

        can, new_pos, reason = self.maze.can_move(self.position, direction)
        if not can:
            return False, reason

        self.position = new_pos

        if self.maze.is_at_end(self.position):
            return True, f"Moved {direction}. Reached the end!"

        return True, f"Moved {direction}"
    
    def get_position(self):
        return self.position

    def get_maze(self):
        return self.maze

    def set_maze(self, maze):
        self.maze = maze
        # Start at the maze's designated start position
        try:
            self.position = tuple(self.maze.start)
        except Exception:
            self.position = (0, 0)

    def detect_walls(self) -> List[str]:
        if self.maze is None:
            return []
        
        walls = []
        for direction in ["up", "down", "left", "right"]:
            can, _, _ = self.maze.can_move(self.position, direction)

    

    