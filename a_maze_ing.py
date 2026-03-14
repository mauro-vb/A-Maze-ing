from a_maze_ing import MazeGenerator

if __name__ == "__main__":
    mazegen = MazeGenerator('sample_config.txt')
    mazegen.generate()
    mazegen.new_render_maze(save=False)
    print(mazegen.get_maze_hex())
