import sys
from pathlib import Path
from src.maze import Maze
from src.mazeRobot import MazeRobot


def main():
    base_dir = Path(__file__).parent
    maze_file = base_dir / "mazes/maze1.json"
    #maze_file = base_dir / "mazes/maze2.json"
    if len(sys.argv) > 1:
        arg_path = Path(sys.argv[1])
        maze_file = arg_path if arg_path.is_absolute() else (base_dir / arg_path)

    maze = Maze(str(maze_file))
    robot = MazeRobot()
    robot.set_maze(maze)

    print(f"Loaded maze {maze_file} (size {maze.width}x{maze.height})")
    print(f"Start: {maze.start}, End: {maze.end}")
    print(f"Robot at {robot.get_position()}")
    print("Enter moves: up/down/left/right, or 'q' to quit.")
    print(maze.render_ascii(robot.get_position()))

    # Manual mode
    while True:
        try:
            cmd = input("> ").strip().lower()
        except EOFError:
            break
        if cmd in ("q", "quit", "exit"):
            break
        if cmd == "pos":
            print(robot.get_position())
            continue
        ok, msg = robot.move(cmd)
        print(msg)
        if ok:
            print(f"Position: {robot.get_position()}")
            print(maze.render_ascii(robot.get_position()))
        if maze.is_at_end(robot.get_position()):
            break


if __name__ == "__main__":
    main()

