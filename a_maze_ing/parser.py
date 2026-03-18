from typing import Dict, Optional, List, Any


class ConfigParser:
    '''Class to parse config file'''
    def __init__(self, config_file: str, parse: bool = True) -> None:
        '''Constructor'''
        # Class attributes
        self.config_file: str = config_file

        # Mandatory fields
        self.WIDTH: int = 0
        self.HEIGHT: int = 0
        self.ENTRY: Dict[Any, Any] = {}
        self.EXIT: Dict[Any, Any] = {}
        self.OUTPUT_FILE: str = ''
        self.PERFECT: bool = False

        # Optional fields
        self.SEED: Optional[int] = None
        self.ALGORITHM: Optional[str] = None
        self.DISPLAY_MODE: Optional[str] = None

        if parse:
            self.parse_config()

    def parse_config(self) -> None:
        '''Parse config file'''
        try:
            with open(self.config_file, 'r') as file:
                for line in file:
                    try:
                        line = line.strip()
                        if line.startswith('#') or line in ['\n', '', '\t']:
                            continue
                        linearr: List[str] = line.split('=')
                        if len(linearr) != 2:
                            raise IndexError(line.strip())
                        key, strvalue = linearr[0].strip(), linearr[1].strip()
                        match key:
                            case "WIDTH":
                                self.assign_width(strvalue)
                            case "HEIGHT":
                                self.assign_height(strvalue)
                            case "ENTRY":
                                self.assign_entry(strvalue)
                            case "EXIT":
                                self.assign_exit(strvalue)
                            case "OUTPUT_FILE":
                                self.OUTPUT_FILE = strvalue.strip()
                            case "PERFECT":
                                self.assign_perfect(strvalue)
                            case "SEED":
                                self.SEED = int(strvalue)
                            case "ALGORITHM":
                                self.assign_algorithm(strvalue)
                            case _:
                                raise KeyError(key)
                    except IndexError as e:
                        print(f"Invalid line: {e}")
                    except KeyError as e:
                        print(f"Invalid key: {e}")
                    except ValueError as e:
                        print(f"Invalid value for {key}: {e}")
        except FileNotFoundError:
            print(f"Could not find {self.config_file}")
            quit()

        except PermissionError:
            print(f"Could not open {self.config_file}, check permissions.")
            quit()
        except Exception as e:
            print(e)
            quit()
        try:
            self.validate_config()
        except AssertionError as e:
            print(f"Invalid config: {e}")
            quit()

    def validate_config(self) -> None:
        '''Checks whether config values are present and valid'''
        assert self.ENTRY != self.EXIT, "ENTRY and EXIT cannot be the same"
        for coord in (self.ENTRY, self.EXIT):
            assert coord['x'] < self.WIDTH, "ENTRY or EXIT is out of bounds"
            assert coord['y'] < self.HEIGHT, "ENTRY or EXIT is out of bounds"
        assert self.WIDTH > 0, "WIDTH must be positive"
        assert self.HEIGHT > 0, "HEIGHT must be positive"
        assert self.ENTRY, "ENTRY is missing"
        assert self.EXIT, "EXIT is missing"
        assert self.OUTPUT_FILE, "OUTPUT_FILE is missing"
        try:
            with open(self.OUTPUT_FILE, 'w') as _:
                pass
        except PermissionError:
            raise AssertionError(
                f"No permission to write to {self.OUTPUT_FILE}"
            )
        except FileNotFoundError:
            raise AssertionError(
                f"Directory does not exist for {self.OUTPUT_FILE}"
            )

    @staticmethod
    def extract_int(strvalue: str) -> int:
        value: int = int(strvalue)
        if value < 0:
            raise ValueError(f"Values must be positive {strvalue}")
        return value

    @staticmethod
    def extract_coords(strvalue: str) -> Dict[Any, Any]:
        vals: List[str] = strvalue.split(',')
        if len(vals) != 2:
            raise ValueError(strvalue)

        return {
            'x': ConfigParser.extract_int(vals[0]),
            'y': ConfigParser.extract_int(vals[1])
        }

    def assign_width(self, strvalue: str) -> None:
        self.WIDTH = self.extract_int(strvalue)

    def assign_height(self, strvalue: str) -> None:
        self.HEIGHT = self.extract_int(strvalue)

    def assign_entry(self, strvalue: str) -> None:
        self.ENTRY = self.extract_coords(strvalue)

    def assign_exit(self, strvalue: str) -> None:
        self.EXIT = self.extract_coords(strvalue)

    def assign_perfect(self, strvalue: str) -> None:
        value: str = strvalue.strip().lower()
        if value == 'true':
            self.PERFECT = True
        elif value == 'false':
            self.PERFECT = False
        else:
            raise ValueError(value)

    def assign_algorithm(self, strvalue: str) -> None:
        if not strvalue.lower() in ('dfs', 'bfs', 'kruskal'):
            raise ValueError(strvalue)
        self.ALGORITHM = strvalue.upper()

    def __str__(self) -> str:
        return (
            f"ConfigParser(\n"
            f"  WIDTH={self.WIDTH}\n"
            f"  HEIGHT={self.HEIGHT}\n"
            f"  ENTRY={self.ENTRY}\n"
            f"  EXIT={self.EXIT}\n"
            f"  OUTPUT_FILE='{self.OUTPUT_FILE}'\n"
            f"  PERFECT={self.PERFECT}\n"
            f"  SEED={self.SEED}\n"
            f"  ALGORITHM={self.ALGORITHM}\n"
            f"  DISPLAY_MODE={self.DISPLAY_MODE}\n"
            f")"
        )
