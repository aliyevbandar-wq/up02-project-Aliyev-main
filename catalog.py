"""Каталог товаров (Фильмы)."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product):
    """Создаёт карточку товара по макету с print-диагностикой."""
    # 🟢 Используем индекс 5, так как в вашей БД это количество товара
    qty = product[5]   
    bg_color = _get_card_color(qty)

    # 📌 ЗАДАНИЕ 5.2: Диагностический вывод в консоль
    print(f"[CARD] id={product[0]}, name={product[2]}, "
          f"qty={qty}, bg={bg_color}, indicator={_indicator(qty)}")

    # Создание самого фрейма карточки
    card = tk.Frame(parent, bg=bg_color, bd=0, 
                    highlightbackground="#CCCCCC", highlightthickness=1)
    
    # ⚠️ ВНИМАНИЕ: Если в вашем main_catalog.py используется card.grid(), 
    # то строку card.pack() ниже нужно закомментировать или удалить!
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    # --- НАЧАЛО ЗАДАНИЯ 6 (Привязка клика) ---
    # Привязка клика к самой карточке
    card.bind("<Button-1>", lambda event: _open_view(parent, product))

    # Привязка клика ко всем дочерним элементам (текст, картинки), 
    # чтобы карточка реагировала на нажатие в любом месте
    for child in card.winfo_children():
        child.bind("<Button-1>", lambda event: _open_view(parent, product))
        # Проходим глубже, если у дочерних элементов есть свои вложенные элементы (например, суб-фреймы)
        for sub_child in child.winfo_children():
            sub_child.bind("<Button-1>", lambda event: _open_view(parent, product))
    # --- КОНЕЦ ЗАДАНИЯ 6 ---

    return card


def _open_view(parent, product):
    """Открывает форму просмотра продукта."""
    from view_form import ViewForm  # Импортируем внутри функции, чтобы избежать кругового импорта
    ViewForm(parent, product)


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 25 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или улучшенную заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    poster_name = product[6]
    image_path = f"resources/{poster_name}" if poster_name else ""

    photo = get_product_image(image_path, size=(100, 140))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo   
        img_label.pack()
    else:
        tk.Label(img_frame, 
                 text="📷\nНет фото", 
                 font=font(FONT_SIZE_NORMAL, bold=True), 
                 fg="#777777", 
                 bg=bg_color,
                 bd=1, 
                 relief="solid", 
                 width=12, 
                 height=7).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию с обработкой сложных крайних случаев."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    genre = product[1] if product[1] else "[Без жанра]"
    raw_name = product[2] if product[2] else "[Без названия]"
    duration = product[3] if product[3] else "[Без длительности]"
    raw_price = product[4] if product[4] is not None else 0

    name = (raw_name[:97] + "...") if len(raw_name) > 100 else raw_name

    if raw_price >= 1000000:
        price_text = f"{raw_price / 1000000:.1f} млн руб."
    else:
        price_text = f"{raw_price} руб."

    duration_text = f"{duration} мин." if isinstance(duration, int) else duration
    
    _add_label(text_frame, f"{duration_text} | {name}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Жанр: {genre}", bg_color)
    _add_label(text_frame, f"В наличии: {_indicator(qty)} ({qty} шт.)", bg_color)
    
    bottom_frame = tk.Frame(text_frame, bg=bg_color)
    bottom_frame.pack(fill="x", side="bottom", pady=5)
    
    # Оставляем только цену, прижатую к левому краю. Кнопка «Купить билет» полностью удалена.
    tk.Label(bottom_frame, text=f"Цена: {price_text}", 
             font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color).pack(side="left")


def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """Вспомогательная микрофункция для добавления стандартной текстовой метки."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 25).
    
    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 25 else "мало"
