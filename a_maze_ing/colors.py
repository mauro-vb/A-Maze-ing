from enum import Enum
from typing import Dict

def getansi(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

class Theme(Enum):
    SEASIDE: Dict = {
        'entry': getansi(231, 236, 239),
        'pattern': getansi(39, 76, 119),
        'exit': getansi(96, 150, 186),
        'walls': getansi(163, 206, 241),
    }
    CANDY: Dict = {
        'entry': getansi(255, 214, 112),
        'pattern': getansi(255, 112, 166),
        'exit': getansi(112, 214, 255),
        'walls': getansi(255, 151, 112),
    }
