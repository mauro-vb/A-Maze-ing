from a_maze_ing import MazeGenerator

if __name__ == "__main__":
    mazegen = MazeGenerator('sample_config.txt')
    mazegen.test_generate()
    mazegen.render_maze(save=True)
