from a_maze_ing import MazeGenerator

if __name__ == "__main__":
    import os
    mazegen = MazeGenerator('sample_config.txt', anim = True)
    mazegen.generate()
    os.system('clear')
    mazegen.new_render_maze()
    print()
    print(mazegen.get_maze_hex())
