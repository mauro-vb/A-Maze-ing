from enum import Enum


def getansi(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"


class Theme(Enum):
    DEFAULT = {
            'entry': getansi(0, 255, 0),
            'pattern': getansi(255, 255, 0),
            'exit': getansi(255, 0, 0),
            'walls': getansi(255, 255, 255),
        }
    SEASIDE = {
        'pattern': getansi(231, 236, 239),
        'entry': getansi(39, 76, 119),
        'exit': getansi(96, 150, 186),
        'walls': getansi(163, 206, 241),
    }
    CANDY = {
        'pattern': getansi(255, 214, 112),
        'walls': getansi(255, 112, 166),
        'exit': getansi(112, 214, 255),
        'entry': getansi(255, 151, 112),
    }
    PASTEL = {
            'entry': getansi(193, 251, 164),
            'pattern': getansi(144, 241, 239),
            'exit': getansi(255, 214, 224),
            'walls': getansi(255, 239, 159),
        }

    ORCHID = {
            'entry': getansi(183, 156, 237),
            'pattern': getansi(149, 127, 239),
            'exit': getansi(239, 217, 206),
            'walls': getansi(222, 192, 241),
        }
