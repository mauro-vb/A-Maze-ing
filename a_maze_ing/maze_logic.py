from .parser import ConfigParser
from typing import List, Optional
from random import seed, randint

class Cell:
    def __init__(
        self,
        walls: int = 15,
        visited:bool = False,
        immutable:bool = False,
        entry: bool = False,
        exit: bool = False
    ) -> None:
        '''Cell initialization'''
        self.walls = walls
        self.visited = visited
        self.immutable = immutable
        self.entry = entry
        self.exit = exit

class MazeGenerator:
    def __init__(self, config_file: str, anim: bool = False) -> None:
        self.config: ConfigParser = ConfigParser(config_file)
        self.anim: bool = anim
        self.maze: List[List[Cell]] = []

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

    def test_generate(self) -> None:
        for row in self.maze:
            for cell in row:
                cell.walls = randint(0, 15)
