from a_maze_ing import MazeGenerator, Theme
from typing import Dict, List, Callable
import os


def user_interface(actions: Dict[str, Callable]) -> None:
    print("\n=== A-Maze-ing ===")
    action_names: List[str] = []
    for i, action_name in enumerate(actions.keys()):
        print(f"{i + 1}. {action_name}")
        action_names.append(action_name)
    choice: str = input(f"Choice? (1-{len(actions)}): ")
    try:
        action: Callable = actions[action_names[int(choice) - 1]]
        action()
    except (ValueError, IndexError):
        print(f"\nPlease enter a valid number...")


def generate_maze(
    anim: bool = True,
    new_seed: bool = False,
    theme: Theme = Theme.DEFAULT
) -> None:
    global maze
    mazegen: MazeGenerator = MazeGenerator(
        'sample_config.txt',
        anim=anim,
        theme=theme,
        new_seed=new_seed
    )
    os.system('clear')
    mazegen.generate()
    os.system('clear')
    mazegen.render_maze()
    maze = mazegen


if __name__ == "__main__":
    animate: bool = True
    show_solution: bool = False
    theme: Theme = Theme.DEFAULT
    maze: MazeGenerator
    generate_maze()

    # Interface
    def regenerate() -> None:
        generate_maze(anim=animate, new_seed=True, theme=theme)

    def toggle_solution() -> None:
        global show_solution
        show_solution= (not show_solution)

    def toggle_animate() -> None:
        global animate
        animate = (not animate)

    def change_theme() -> None:
        for i, t in enumerate(Theme):
            print(f"{i + 1}. {t.name}")
        try:
            global theme
            themes: List = list(Theme)
            theme = themes[int(input(f"Choice? (1 - {len(Theme)}): ")) - 1]
        except (ValueError, IndexError):
            print(f"\nPlease enter a valid number...")

    def quit_program() -> None:
        os.system('clear')
        quit()

    while True:
        os.system('clear')
        maze.render_maze()
        actions: Dict[str, Callable] = {
            "Generate new maze": regenerate,
            f"{'Disable' if animate else 'Enable'} animation": toggle_animate,
            "Change color theme": change_theme,
            f"{'Hide' if show_solution else 'Show'} solution": toggle_solution,
            "Quit": quit_program
        }
        user_interface(actions)
