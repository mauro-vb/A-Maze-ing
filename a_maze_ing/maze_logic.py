from .parser import ConfigParser
from typing import List, Optional, Tuple
from random import seed, randint

pattern_42: Tuple[Tuple[int, int]] = (
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 0),
    (2, 1), (2, 2), (2, 3), (2, 4),  # '4'
    (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
    (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)  # '2'
)

class Cell:
    def __init__(
        self,
        walls: int = 15,
        visited:bool = False,
        immutable:bool = False,
        entry: bool = False,
        exit: bool = False,
    ) -> None:
        '''Cell initialization'''
        self.walls: int = walls
        self.visited: bool = visited
        self.immutable: bool = immutable
        self.entry: bool = entry
        self.exit:bool = exit
        self.pattern = pattern_42

class MazeGenerator:
    def __init__(
        self,
        config_file: str,
        anim: bool = False,
        pattern: Tuple[Tuple[int, int]] = pattern_42
    ) -> None:
        self.config: ConfigParser = ConfigParser(config_file)
        self.anim: bool = anim
        self.maze: List[List[Cell]] = []
        self.pattern = pattern
        s: Optional[int] = self.config.SEED
        seed(randint(0, 99999999) if s is None else s)
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


    def render_maze(self, save: bool = False, wall_char: str = '█') -> None:
        render: str = ''
        w: str = wall_char
        hwall: str = f'{w}{w}{w}'
        hopen: str = '   '
        vwall: str = f'{w}'
        vopen: str = ' '
        for row in self.maze:
            line1: str = ''
            line2: str = ''
            for cell in row:
                cellcontent: str = hopen
                if cell.entry or cell.exit:
                    cellcontent = ' ● ' if cell.entry else ' * '

                # 1st line
                north: str = hwall if (cell.walls & (1 << 0)) else hopen
                east: str = vwall if (cell.walls & (1 << 1)) else vopen
                west: str = vwall if (cell.walls & (1 << 3)) else vopen
                line1 += west + north + east

                # 2nd line
                east: str = vwall if (cell.walls & (1 << 1)) else vopen
                south: str = hwall if (cell.walls & (1 << 2)) else cellcontent
                west: str = vwall if (cell.walls & (1 << 3)) else vopen
                line2 += west + south + east

            rowstr: str = line1 + '\n' + line2 + '\n'
            if save:
                render += rowstr
            else:
                print(rowstr, end='')

        bottomwall: str = f'{w}{w}{w}{w}{w}' * self.config.WIDTH
        if save:
            with open(self.config.OUTPUT_FILE, 'w') as file:
                file.write(render + bottomwall)
        else:
            print(bottomwall)

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
