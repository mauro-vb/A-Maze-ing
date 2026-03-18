from .parser import ConfigParser
from .colors import Theme
from typing import List, Optional, Tuple, Dict, Any, Set
from random import seed, randint, choice, shuffle
import time

pattern_42: Tuple[Tuple[int, int], ...] = (
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 0),
    (2, 1), (2, 2), (2, 3), (2, 4),  # '4'
    (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
    (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)  # '2'
)


class Cell:
    def __init__(
        self,
        walls: int = 15,
        visited: bool = False,
        immutable: bool = False,
        entry: bool = False,
        exit: bool = False,
    ) -> None:
        '''Cell initialization'''
        self.walls: int = walls
        self.visited: bool = visited
        self.immutable: bool = immutable
        self.entry: bool = entry
        self.exit: bool = exit
        self.path: bool = False
        self.solution: bool = False


class MazeGenerator:
    def __init__(
        self,
        config_file: str,
        anim: bool = False,
        theme: Theme = Theme.SEASIDE,
        new_seed: bool = False,
        pattern: Tuple[Tuple[int, int], ...] = pattern_42
    ) -> None:
        self.config: ConfigParser = ConfigParser(config_file)
        self.solution: List[Cell] = []
        self.anim: bool = anim
        self.maze: List[List[Cell]] = []
        self.pattern = pattern
        s: Optional[int] = self.config.SEED
        seed(randint(0, 99999999) if s is None or new_seed else s)
        self.change_theme(theme)
        self.maze_init()

    def change_theme(self, theme: Theme) -> None:
        value: Dict[Any, Any] = theme.value
        self.wall_color = value['walls']
        self.pattern_color = value['pattern']
        self.exit_color = value['exit']
        self.entry_color = value['entry']

    def maze_init(self) -> None:
        '''Initializes maze grid'''
        entry: Tuple[Any, Any] = (self.config.ENTRY['x'],
                                  self.config.ENTRY['y'])
        exit: Tuple[Any, Any] = (self.config.EXIT['x'],  self.config.EXIT['y'])
        for y in range(self.config.HEIGHT):
            row: List[Cell] = []
            for x in range(self.config.WIDTH):
                isentry: bool = entry == (x, y)
                isexit: bool = exit == (x, y)
                row.append(Cell(entry=isentry, exit=isexit))
            self.maze.append(row)
        pwidth: int = max(self.pattern, key=lambda pos: pos[0])[0]
        pheight: int = max(self.pattern, key=lambda pos: pos[1])[1]
        self.size = self.config.WIDTH * self.config.HEIGHT
        if self.config.WIDTH > pwidth and self.config.HEIGHT > pheight:
            x_offset: int = (self.config.WIDTH - pwidth) // 2
            y_offset: int = (self.config.HEIGHT - pheight) // 2
            for x, y in self.pattern:
                cell: Cell = self.maze[y + y_offset][x + x_offset]
                if cell.entry or cell.exit:
                    print("Entry and Exit cannot be on pattern.")
                    return
                cell.walls = 15
                cell.visited = True
                cell.immutable = True
        else:
            print("Could not draw pattern, maze is too small...")

    def render_maze(self, save: bool = False) -> None:
        RESET = '\033[0m'
        render: str = "\n"
        wall_char: str = f'{self.wall_color}█{RESET}'
        for y, row in enumerate(self.maze):
            top_line = ""
            mid_line = ""
            for x, cell in enumerate(row):
                if cell.entry:
                    content = f"{self.entry_color} ⬤ {RESET}"
                elif cell.exit:
                    content = f"{self.exit_color} ⬤ {RESET}"
                elif cell.immutable:
                    content = f"{self.pattern_color}███{RESET}"
                elif cell.solution:
                    content = f"{self.entry_color} ■ {RESET}"
                elif cell.path:
                    content = f"{self.exit_color} ▪ {RESET}"
                else:
                    content = "   "
                corner = wall_char
                north = wall_char * 3 if (cell.walls & 1) else "   "
                top_line += f"{corner}{north}"
                west = wall_char if (cell.walls & 8) else " "
                mid_line += f"{west}{content}"
                if x == self.config.WIDTH - 1:
                    top_line += corner
                    east = wall_char if (cell.walls & 2) else " "
                    mid_line += east
            render += top_line + "\n" + mid_line + "\n"
        bottom_line = ""
        for cell in self.maze[-1]:
            corner = wall_char
            south = wall_char * 3 if (cell.walls & 4) else "   "
            bottom_line += f"{corner}{south}"
        bottom_line += wall_char
        render += bottom_line
        if save:
            pass
        else:
            print(render, end='')

    def get_maze_hex(self) -> str:
        maze_hex: str = ''
        for row in self.maze:
            line: str = ''
            for cell in row:
                line += f'{cell.walls:X}'
            maze_hex += line + '\n'
        return maze_hex

    def test_generate(self) -> None:
        for row in self.maze:
            for cell in row:
                if cell.immutable:
                    continue
                cell.walls = 0

    def generate(self) -> None:
        algo: Optional[str] = self.config.ALGORITHM
        if not algo or algo == 'DFS':
            self._generate_dfs()
        elif algo == 'BFS':
            self._generate_bfs()
        elif algo == 'KRUSKAL':
            self._generate_kruskal()
        if not self.config.PERFECT:
            self._turn_imperfect()

        with open(self.config.OUTPUT_FILE, 'w') as file:
            file.write(self.get_maze_hex())

    def _update_frame(self) -> None:
        self.render_maze()
        time.sleep(0.025)
        lines_up = (self.config.HEIGHT * 2) + 1
        print(f'\033[{lines_up}F', end='', flush=True)

    def _get_unvisited_neighbors(
        self, x: int, y: int
    ) -> List[Tuple[int, int, str]]:
        neighbors: List[Tuple[int, int, str]] = []
        if y > 0 and not self.maze[y - 1][x].visited:
            neighbors.append((x, y - 1, 'N'))
        if x < self.config.WIDTH - 1 and not self.maze[y][x + 1].visited:
            neighbors.append((x + 1, y, 'E'))
        if y < self.config.HEIGHT - 1 and not self.maze[y + 1][x].visited:
            neighbors.append((x, y + 1, 'S'))
        if x > 0 and not self.maze[y][x - 1].visited:
            neighbors.append((x - 1, y, 'W'))
        return neighbors

    def _get_accessible_neighbors(
        self, x: int, y: int
    ) -> List[Tuple[int, int]]:
        cell = self.maze[y][x]
        neighbors = []

        if not cell.walls & 1:
            neighbors.append((x, y - 1))
        if not cell.walls & 2:
            neighbors.append((x + 1, y))
        if not cell.walls & 4:
            neighbors.append((x, y + 1))
        if not cell.walls & 8:
            neighbors.append((x - 1, y))

        return neighbors

    def _turn_imperfect(self) -> None:
        def inbounds_and_not_immutable(y: int, x: int) -> bool:
            if x < 0 or x >= len(self.maze[0]):
                return False
            if y < 0 or y >= len(self.maze):
                return False
            if self.maze[y][x].immutable:
                return False
            return True

        def n_walls(cell: Cell) -> int:
            return bin(cell.walls).count('1')

        dirs: Dict[int, Tuple[int, int]] = {
            1: (-1, 0),
            2: (0, 1),
            4: (1, 0),
            8: (0, -1)
        }
        opposite: Dict[int, int] = {1: 4, 2: 8, 4: 1, 8: 2}
        removed: int = 0
        target_removals: int = randint(
            max(1, int(self.size * 0.025)),
            int(self.size * 0.05)
        )
        while removed < target_removals:
            x: int = randint(0, len(self.maze[0]) - 1)
            y: int = randint(0, len(self.maze) - 1)
            cell: Cell = self.maze[y][x]
            if cell.immutable:
                continue
            dir: int = choice(list(dirs.keys()))
            ny, nx = dirs[dir][0] + y, dirs[dir][1] + x
            if not inbounds_and_not_immutable(ny, nx):
                continue
            neighbor: Cell = self.maze[ny][nx]
            if not (cell.walls & dir) or not (neighbor.walls & opposite[dir]):
                continue
            if n_walls(cell) + n_walls(neighbor) <= 3:
                continue
            cell.walls &= ~dir
            neighbor.walls &= ~opposite[dir]
            removed += 1
            if self.anim:
                self._update_frame()

    def _remove_wall(
        self, cx: int, cy: int, nx: int, ny: int, direction: str
    ) -> None:
        current_cell = self.maze[cy][cx]
        next_cell = self.maze[ny][nx]
        if direction == 'N':
            current_cell.walls &= ~1
            next_cell.walls &= ~4
        elif direction == 'E':
            current_cell.walls &= ~2
            next_cell.walls &= ~8
        elif direction == 'S':
            current_cell.walls &= ~4
            next_cell.walls &= ~1
        elif direction == 'W':
            current_cell.walls &= ~8
            next_cell.walls &= ~2

    def _generate_dfs(self) -> None:
        from random import choice

        start_x: int = self.config.ENTRY['x']
        start_y: int = self.config.ENTRY['y']
        stack: List[Tuple[int, int]] = [(start_x, start_y)]
        self.maze[start_y][start_x].visited = True
        while stack:
            current_x, current_y = stack.pop()
            neighbors = self._get_unvisited_neighbors(current_x, current_y)
            if neighbors:
                stack.append((current_x, current_y))
                next_x, next_y, direction = choice(neighbors)
                self._remove_wall(
                    current_x, current_y, next_x, next_y, direction
                )
                self.maze[next_y][next_x].visited = True
                stack.append((next_x, next_y))
                if self.anim:
                    self._update_frame()

    def _generate_bfs(self) -> None:
        from random import shuffle
        from collections import deque

        start_x: int = self.config.ENTRY['x']
        start_y: int = self.config.ENTRY['y']
        queue: deque[Tuple[int, int]] = deque([(start_x, start_y)])
        self.maze[start_y][start_x].visited = True
        while queue:
            current_x, current_y = queue.popleft()
            neighbors = self._get_unvisited_neighbors(current_x, current_y)
            shuffle(neighbors)
            for next_x, next_y, direction in neighbors:
                if not self.maze[next_y][next_x].visited:
                    self._remove_wall(
                        current_x, current_y, next_x, next_y, direction
                    )
                    self.maze[next_y][next_x].visited = True
                    queue.append((next_x, next_y))

    def _generate_kruskal(self) -> None:
        WIDTH: int = self.config.WIDTH
        HEIGHT: int = self.config.HEIGHT
        parent: dict[Tuple[int, int], Tuple[int, int]] = {}
        rank: dict[Tuple[int, int], int] = {}

        def find(i: Tuple[int, int]) -> Tuple[int, int]:
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i: Tuple[int, int], j: Tuple[int, int]) -> bool:
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                if rank[root_i] > rank[root_j]:
                    parent[root_j] = root_i
                elif rank[root_i] < rank[root_j]:
                    parent[root_i] = root_j
                else:
                    parent[root_j] = root_i
                    rank[root_i] += 1
                return True
            return False
        edges: List[Tuple[Tuple[int, int], Tuple[int, int], str]] = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.maze[y][x].immutable:
                    continue
                cell_id = (x, y)
                parent[cell_id] = cell_id
                rank[cell_id] = 0

                if x < WIDTH - 1 and not self.maze[y][x+1].immutable:
                    edges.append(((x, y), (x + 1, y), 'E'))
                if y < HEIGHT - 1 and not self.maze[y + 1][x].immutable:
                    edges.append(((x, y), (x, y + 1), 'S'))
        shuffle(edges)
        for (cx, cy), (nx, ny), direction in edges:
            if union((cx, cy), (nx, ny)):
                self._remove_wall(cx, cy, nx, ny, direction)
                self.maze[cy][cx].visited = True
                self.maze[ny][nx].visited = True
                if self.anim:
                    self._update_frame()

    def _solve_bfs(self) -> None:
        from collections import deque

        start_x: int = self.config.ENTRY['x']
        start_y: int = self.config.ENTRY['y']
        end: Tuple[int, int] = (self.config.EXIT['x'], self.config.EXIT['y'])
        queue: deque[Tuple[int, int]] = deque([(start_x, start_y)])
        visited: Set[Any] = set()
        parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
        self.maze[start_y][start_x].visited = True
        while queue:
            current_x, current_y = queue.popleft()
            self.maze[current_y][current_x].path = True
            if self.anim:
                self._update_frame()
            if (current_x, current_y) == end:
                break

            neighbors = self._get_accessible_neighbors(current_x, current_y)
            for next_x, next_y in neighbors:
                if (next_x, next_y) not in visited:
                    parent[(next_x, next_y)] = (current_x, current_y)
                    queue.append((next_x, next_y))
                    visited.add((next_x, next_y))

        path: List[Cell] = []
        cell: Tuple[int, int] = end
        while cell != (start_x, start_y):
            cell_o = self.maze[cell[1]][cell[0]]
            path.append(cell_o)
            cell_o.solution = True
            if self.anim:
                self._update_frame()
            cell = parent[cell]

        self.solution = path
        for x, y in visited:
            self.maze[y][x].path = False

    def toggle_solution(self, show: bool) -> None:
        if not self.solution:
            self._solve_bfs()
        for cell in self.solution:
            cell.solution = show
        self.render_maze()
