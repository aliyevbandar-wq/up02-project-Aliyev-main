"""Стили приложения по руководству КИМ."""
import tkinter as tk

# =====================================================================
# Цвета из руководства по стилю
# =====================================================================
COLOR_MAIN_BG = "#FFFFFF"       # основной фон
COLOR_SECONDARY_BG = "#D2F6E7"  # дополнительный фон
COLOR_ACCENT = "#70B2AF"        # акцент
COLOR_HIGHLIGHT = "#ff8080"     # подсветка ≤3

# =====================================================================
# Константы шрифтов по руководству КИМ
# =====================================================================
FONT_FAMILY = "Calibri"
FONT_SIZE_SMALL = 10
FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 14
FONT_SIZE_TITLE = 18


def font(family_or_size=FONT_SIZE_NORMAL, size=None, weight=None, bold=False):
    """Возвращает кортеж шрифта, совместимый с макетом КИМ и кодом окон."""
    if isinstance(family_or_size, str):
        actual_family = family_or_size
        actual_size = size if size is not None else FONT_SIZE_NORMAL
        is_bold = (weight == "bold" or bold)
    else:
        actual_family = FONT_FAMILY
        actual_size = family_or_size
        is_bold = bold

    return (actual_family, actual_size, "bold" if is_bold else "normal")


def make_button(parent, text, command):
    """Кнопка в стиле КИМ."""
    return tk.Button(
        parent, text=text, command=command,
        bg=COLOR_ACCENT, fg="white",
        font=font(FONT_SIZE_NORMAL),
        relief="flat", padx=15, pady=5,
        activebackground=COLOR_ACCENT,
        cursor="hand2"
    )
