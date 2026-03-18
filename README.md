*This project has been created as part of the 42 curriculum by mvazquez, mpeskov.*

## Description

**A-Maze-ing** is a Python-based procedural maze generator and solver.
Maze generation serves as a practical application of algorithms, randomness, and graph theory, demonstrating how computers can create structure from chaos.

This tool reads a configuration file, generates a maze (either a "perfect" maze with one unique path, or an imperfect one), and writes the result to a file using a specialized hexadecimal wall representation. It also includes a visual CLI representation featuring customizable themes, real-time generation animations, and a mandatory structural "42" pattern integrated directly into the maze structure.

-----

## Instructions

### Prerequisites

  * **Python**: Your environment must be running Python 3.10 or later.
  * **Dependencies**: The project requires a few standard linting and building packages: `flake8`, `mypy`, `setuptools`, and `build`.

### Installation

A `Makefile` is included to automate common tasks.

  * To install the required project dependencies and make use of all the functionality, run:
    ```bash
    make install
    source ./venv/bin/activate
    ```

### Execution

You can run the main program using the Makefile:

```bash
make run
```

Or you can execute it manually by passing your configuration file as the only argument:
```bash
python3 a_maze_ing.py config.txt
```


### Development & Linting

  * Clean temporary files and caches (`__pycache__`, `.mypy_cache`): `make clean`.
  * Run static analysis and linting: `make lint`.

-----

## Configuration File Format

The configuration file strictly requires one `KEY=VALUE` pair per line. Any line beginning with `#` is treated as a comment and will be ignored.

The following keys are mandatory for the program to run successfully:

| Key | Description | Example |
| :--- | :--- | :--- |
| **WIDTH** | Maze width (number of cells) | `WIDTH=20` |
| **HEIGHT** | Maze height | `HEIGHT=15` |
| **ENTRY** | Entry coordinates (x,y) | `ENTRY=0,0` |
| **EXIT** | Exit coordinates (x,y) | `EXIT=19,14` |
| **OUTPUT\_FILE** | Output filename | `OUTPUT_FILE=maze.txt` |
| **PERFECT** | Is the maze perfect? | `PERFECT=True` |

-----

## Output File Format

The program writes the generated maze to the specified `OUTPUT_FILE`. [cite_start]The output relies on a hexadecimal encoding system where each digit represents a single cell and encodes which of its walls are closed[cite: 147]:

  * **Bit 0 (LSB)**: North [cite: 148]
  * **Bit 1**: East [cite: 148]
  * **Bit 2**: South [cite: 148]
  * **Bit 3**: West [cite: 148]

A closed wall sets the bit to `1`, while an open wall sets it to `0`. The cells are stored row by row. After the maze layout, an empty line is inserted, followed by the entry coordinates, exit coordinates, and the shortest valid path from start to end using the letters `N, E, S, W`.

-----

## Algorithms Chosen

This project implements three distinct maze generation algorithms: **DFS (Depth-First Search)**, **BFS (Breadth-First Search)**, and **Kruskal's Algorithm**.

  * **Why these were chosen:**
  * **DFS** (Recursive Backtracker) was chosen for its characteristic long, winding corridors, making the maze visually appealing and fun for humans to solve.
  * **Kruskal's Algorithm** creates highly branched mazes with many short dead ends. Because perfect mazes are directly related to spanning trees in graph theory, Kruskal's is an ideal mathematical approach to ensure full connectivity.
   * **BFS** was chosen both as a generation alternative for radiating patterns and as the core logic for the solver (`_solve_bfs`) to guarantee the shortest possible path between the entry and exit.

-----

## Code Reusability

The architecture separates the interactive Command-Line Interface (`a_maze_ing.py`) from the core generation logic (`maze_logic.py`).

  * **How to reuse:** The `MazeGenerator` and `Cell` classes can be imported directly into any other Python 3.10+ application without triggering the CLI.
  ```bash
  make package
  ```

    ```python
    from a_maze_ing import MazeGenerator, Theme

    # Initialize a maze programmatically
    generator = MazeGenerator(config_file="config.txt", theme=Theme.DEFAULT)
    generator.generate()
    ```

This modularity ensures the generation logic can be easily integrated into future UI frameworks, video games, or network design simulators.

-----

## Advanced Features

  * **Interactive UI:** An in-terminal menu allowing users to generate new mazes, toggle generation animations, change color themes (like `SEASIDE`), and hide/show the shortest path solution.
  * **Imperfect Mazes:** If `PERFECT=False` is set in the configuration, the program dynamically breaks additional walls to create multiple valid paths while ensuring no massive open areas are formed.
  * **Visual Pattern:** Automatically embeds a structural "42" pattern constructed of immutable, fully walled cells within the maze, dynamically calculating offsets to center it.

-----

## Team and Project Management

  * **Roles:** `mpeskov` focused on the core graph theory algorithms (DFS/BFS/Kruskal) and hex-encoding. `mvazquez` built the interactive CLI, animation logic, and the BFS solver.
  * **Planning & Evolution:** We initially planned to only implement DFS, but finished ahead of schedule and added Kruskal's to better understand spanning trees.
  * **Successes & Improvements:** Peer debugging the hexadecimal bitwise operators worked extremely well. In the future, we could improve the visual rendering performance for extremely large mazes.
  * **Tools Used:** We relied on Git for version control and `flake8`/`mypy` for strict type enforcement and linting.

-----

## Resources

  * **References:**
  * *Maze Generation Algorithms* (Wikipedia)
  * *Graph Theory and Spanning Trees*
  * **AI Usage:** AI was utilized to reduce repetitive and tedious tasks during development, such as writing baseline boilerplate for the `setup.py` and README.md rewriting. No AI-generated code was copy-pasted blindly, ensuring full credibility and understanding of the project.
