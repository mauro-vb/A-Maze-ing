from a_maze_ing import MazeGenerator

if __name__ == "__main__":
    mazegen = MazeGenerator('sample_config.txt', anim = True)
    mazegen.generate()
    print(mazegen.get_maze_hex())
