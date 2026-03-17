from .parser import ConfigParser
from .colors import Theme
from typing import List, Optional, Tuple, Dict
from random import seed, randint

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
        self.pattern = pattern_42


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
        self.anim: bool = anim
        self.maze: List[List[Cell]] = []
        self.pattern = pattern
        s: Optional[int] = self.config.SEED
        seed(randint(0, 99999999) if s is None or new_seed else s)
        value: Dict = theme.value
        self.wall_color = value['walls']
        self.pattern_color = value['pattern']
        self.exit_color = value['exit']
        self.entry_color = value['entry']
        self.maze_init()

    def maze_init(self) -> None:
        '''Initializes maze grid'''
        entry: Tuple = (self.config.ENTRY['x'],  self.config.ENTRY['y'])
        exit: Tuple = (self.config.EXIT['x'],  self.config.EXIT['y'])
        for y in range(self.config.HEIGHT):
            row: List[Cell] = []
            for x in range(self.config.WIDTH):
                isentry: bool = entry == (x, y)
                isexit: bool = exit == (x, y)
                row.append(Cell(entry=isentry, exit=isexit))
            self.maze.append(row)
        pwidth: int = max(self.pattern, key=lambda pos: pos[0])[0]
        pheight: int = max(self.pattern, key=lambda pos: pos[1])[1]

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


    def new_render_maze(
        self, save: bool = False
    ) -> None:
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

#    def render_maze(self, save: bool = False, wall_char: str = '█') -> None:
#        render: str = ''
#        w: str = wall_char
#        hwall: str = f'{w}{w}{w}'
#        hopen: str = '   '
#        vwall: str = f'{w}'
#        vopen: str = ' '
#        for row in self.maze:
#            line1: str = ''
#            line2: str = ''
#            for cell in row:
#                cellcontent: str = hopen
#                if cell.entry or cell.exit:
#                    cellcontent = ' ● ' if cell.entry else ' * '
#
#                # 1st line
#                north: str = hwall if (cell.walls & (1 << 0)) else hopen
#                east: str = vwall if (cell.walls & (1 << 1)) else vopen
#                west: str = vwall if (cell.walls & (1 << 3)) else vopen
#                line1 += west + north + east
#
#                # 2nd line
#                east: str = vwall if (cell.walls & (1 << 1)) else vopen
#                south: str = hwall if (cell.walls & (1 << 2)) else cellcontent
#                west: str = vwall if (cell.walls & (1 << 3)) else vopen
#                line2 += west + south + east
#
#            rowstr: str = line1 + '\n' + line2 + '\n'
#            if save:
#                render += rowstr
#            else:
#                print(rowstr, end='')
#
#        bottomwall: str = f'{w}{w}{w}{w}{w}' * self.config.WIDTH
#        if save:
#            with open(self.config.OUTPUT_FILE, 'w') as file:
#                file.write(render + bottomwall)
#        else:
#            print(bottomwall)

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
        import time
        # import os

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
                    print('\033[H', end='')
                    self.new_render_maze()
                    time.sleep(0.025)

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
        from random import shuffle
        import time
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
        for y in range(self.config.HEIGHT):
            for x in range(self.config.WIDTH):
                if self.maze[y][x].immutable:
                    continue
                cell_id = (x, y)
                parent[cell_id] = cell_id
                rank[cell_id] = 0
                if x < self.config.WIDTH - 1 and not self.maze[y][x+1].immutable:
                    edges.append(((x, y), (x + 1, y), 'E'))
                if y < self.config.HEIGHT - 1 and not self.maze[y + 1][x].immutable:
                    edges.append(((x, y), (x, y + 1), 'S'))
        shuffle(edges)
        for (cx, cy), (nx, ny), direction in edges:
            if union((cx, cy), (nx, ny)):
                self._remove_wall(cx, cy, nx, ny, direction)
                self.maze[cy][cx].visited = True
                self.maze[ny][nx].visited = True
                if self.anim:
                    print('\033[H', end='')
                    self.new_render_maze()
                    time.sleep(0.05)
