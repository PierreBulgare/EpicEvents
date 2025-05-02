from colorama import init, Fore, Back, Style


class TextManager:
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
    }

    background_map = {
        "red": Back.RED,
        "green": Back.GREEN,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "magenta": Back.MAGENTA,
        "cyan": Back.CYAN,
        "white": Back.WHITE,
        "black": Back.BLACK,
    }

    style_map = {
        "bold": Style.BRIGHT,
        "dim": Style.DIM,
        "normal": Style.NORMAL,
    }

    @staticmethod
    def init_colorama():
        init(autoreset=True)

    @classmethod
    def color(cls, text, color):
        return f"{cls.color_map.get(color, Fore.WHITE)}{text}"
    
    @classmethod
    def background(cls, text, color):
        return f"{cls.background_map.get(color, Back.RESET)}{text}"

    @classmethod
    def style(cls, text, style):
        return f"{cls.style_map.get(style, Style.NORMAL)}{text}"
