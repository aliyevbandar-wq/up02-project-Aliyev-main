"""Каталог товаров (Фильмы)."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку товара по макету с print-диагностикой."""
    # Получаем количество товара из индекса 5 вашей БД
    qty = product[5] if (hasattr(product, '__getitem__') and len(product) > 5) else 0
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=0, 
                    highlightbackground="#CCCCCC", highlightthickness=1)
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    # Привязка кликов для открытия формы
    card.bind("<Button-1>", lambda event: _open_view(parent, product, refresh))

    for child in card.winfo_children():
        child.bind("<Button-1>", lambda event: _open_view(parent, product, refresh))
        for sub_child in child.winfo_children():
            sub_child.bind("<Button-1>", lambda event: _open_view(parent, product, refresh))

    return card


def _open_view(parent, product, refresh=None):
    """Открывает форму просмотра продукта."""
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 25 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара из индекса 6."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Берём точное имя файла картинки из индекса 6 базы данных
    poster_name = product[6] if (hasattr(product, '__getitem__') and len(product) > 6) else ""
    image_path = f"resources/{poster_name}" if poster_name else ""

    photo = get_product_image(image_path, size=(100, 140))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo   
        img_label.pack()
    else:
        tk.Label(img_frame, text="📷\nНет фото", font=font(FONT_SIZE_NORMAL, bold=True), 
                 fg="#777777", bg=bg_color, bd=1, relief="solid", width=12, height=7).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    genre = product[1] if (hasattr(product, '__getitem__') and len(product) > 1) else "[Без жанра]"
    raw_name = product[2] if (hasattr(product, '__getitem__') and len(product) > 2) else "[Без названия]"
    duration = product[3] if (hasattr(product, '__getitem__') and len(product) > 3) else "120"
    raw_price = product[4] if (hasattr(product, '__getitem__') and len(product) > 4) else 0

    name = (str(raw_name)[:97] + "...") if len(str(raw_name)) > 100 else str(raw_name)
    price_text = f"{raw_price} руб."
    duration_text = f"{duration} мин." if isinstance(duration, int) else str(duration)
    
    _add_label(text_frame, f"{duration_text} | {name}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Жанр: {genre}", bg_color)
    _add_label(text_frame, f"В наличии: {_indicator(qty)} ({qty} шт.)", bg_color)
    
    bottom_frame = tk.Frame(text_frame, bg=bg_color)
    bottom_frame.pack(fill="x", side="bottom", pady=5)
    
    tk.Label(bottom_frame, text=f"Цена: {price_text}", 
             font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color).pack(side="left")


def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL):
    lbl = tk.Label(parent, text=text, font=font(size, bold=bold), bg=bg_color, anchor="w")
    lbl.pack(fill="x")


def _indicator(qty):
    return "много" if qty > 25 else "мало"
