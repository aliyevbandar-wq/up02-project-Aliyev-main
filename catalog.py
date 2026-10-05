"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # type: ignore
import os

from config import DB_PATH, COLOR_HIGHLIGHT, FONT_FAMILY
import db_loader as db


def create_product_card(parent, product):
    """
    Создаёт карточку товара по макету.
    
    :param parent: родительский контейнер
    :param product: кортеж из БД (id, жанр, название, длительность, цена, количество, постер)
    """
    # Вытягиваем данные по вашим индексам из БД SQLite
    genre = product[1]         # Жанр (Категория)
    name = product[2]          # Название (Наименование)
    duration = product[3]      # Длительность (Производство / Состав)
    price = product[4]         # Цена
    qty = product[5]           # Количество
    poster_name = product[6]   # Имя файла постера

    # Определяем фон: подсветка, если количество ≤ 15 (для фильмов снизим порог, т.к. остатки небольшие)
    bg_color = COLOR_HIGHLIGHT if qty <= 15 else "white"

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # --- ЗАДАНИЕ 6.3: Проверка существования файла постера ---
    image_path = f"resources/{poster_name}" if poster_name else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 140)) # Фильм-постер лучше делать вертикальным (100х140)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ПОСТЕР]", bg=bg_color,
                 width=10, height=7).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Длительность | Название фильма (Вместо Производство | Наименование)
    title = f"{duration} мин. | {name}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    # Жанр (Вместо Категория)
    tk.Label(text_frame, text=f"Жанр: {genre}",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Количество
    indicator = "много" if qty > 20 else "мало"
    tk.Label(text_frame, text=f"В наличии: {indicator} ({qty} шт.)",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Длительность дублируем в Состав или оставляем прочерк
    tk.Label(text_frame, text=f"Продолжительность: {duration} мин.",
             font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")

    # Цена (справа)
    tk.Label(text_frame, text=f"Цена: {price} руб.",
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="e").pack(fill="x")

    return card
