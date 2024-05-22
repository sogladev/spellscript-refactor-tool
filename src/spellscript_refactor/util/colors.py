from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4

def color(text, color, end='\n') -> str:
    colors = {Color.RED: '\x1b[31m', Color.GREEN: '\x1b[32m', Color.YELLOW: '\x1b[33m', Color.BLUE: '\x1b[34m'}
    reset = '\x1b[0m'
    return colors.get(color, '') + text + reset + end