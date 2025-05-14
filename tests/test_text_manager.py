import pytest
from messages_managers.text import TextManager
from colorama import init, Fore, Back, Style

def test_color_valid_color():
    text = "Test"
    color = "red"
    TextManager.color_map = {"red": Fore.RED}
    result = TextManager.color(text, color)
    assert result == f"{Fore.RED}{text}"

def test_color_invalid_color():
    text = "Test"
    color = ""
    TextManager.color_map = {"red": Fore.RED}
    result = TextManager.color(text, color)
    assert result == f"{Fore.WHITE}{text}"

def test_color_no_color_map():
    text = "Test"
    color = "red"
    TextManager.color_map = {}
    result = TextManager.color(text, color)
    assert result == f"{Fore.WHITE}{text}"

def test_background_valid_color():
    text = "Test"
    color = "red"
    TextManager.background_map = {"red": Back.RED}
    result = TextManager.background(text, color)
    assert result == f"{Back.RED}{text}"

def test_background_invalid_color():
    text = "Test"
    color = ""
    TextManager.background_map = {"red": Back.RED}
    result = TextManager.background(text, color)
    assert result == f"{Back.RESET}{text}"

def test_background_no_color_map():
    text = "Test"
    color = "red"
    TextManager.background_map = {}
    result = TextManager.background(text, color)
    assert result == f"{Back.RESET}{text}"

def test_style_valid_style():
    text = "Test"
    style = "bold"
    TextManager.style_map = {"bold": Style.BRIGHT}
    result = TextManager.style(text, style)
    assert result == f"{Style.BRIGHT}{text}"

def test_style_invalid_style():
    text = "Test"
    style = ""
    TextManager.style_map = {"bold": Style.BRIGHT}
    result = TextManager.style(text, style)
    assert result == f"{Style.NORMAL}{text}"

def test_style_no_style_map():
    text = "Test"
    style = "bold"
    TextManager.style_map = {}
    result = TextManager.style(text, style)
    assert result == f"{Style.NORMAL}{text}"