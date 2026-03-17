from enum import Enum
from typing import Dict

def getansi(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

class Theme(Enum):
    DEFAULT: Dict = {
            'entry': getansi(0, 255, 0),
            'pattern': getansi(255, 255, 0),
            'exit': getansi(255, 0, 0),
            'walls': getansi(255, 255, 255),
        }
    SEASIDE: Dict = {
        'entry': getansi(231, 236, 239),
        'pattern': getansi(39, 76, 119),
        'exit': getansi(96, 150, 186),
        'walls': getansi(163, 206, 241),
    }
    CANDY: Dict = {
        'entry': getansi(255, 214, 112),
        'exit': getansi(255, 112, 166),
        'walls': getansi(112, 214, 255),
        'pattern': getansi(255, 151, 112),
    }
    PASTEL: Dict = {
            'entry': getansi(193, 251, 164),
            'pattern': getansi(144, 241, 239),
            'exit': getansi(255, 214, 224),
            'walls': getansi(255, 239, 159),
        }

    ORCHID: Dict = {
            'entry': getansi(183, 156, 237),
            'pattern': getansi(149, 127, 239),
            'exit': getansi(239, 217, 206),
            'walls': getansi(222, 192, 241),
        }
