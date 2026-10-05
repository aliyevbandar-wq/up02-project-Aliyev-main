"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # type: ignore
import os

from config import COLOR_HIGHLIGHT, FONT_FAMILY


def create_product_card(parent, product):
    """Создаёт карточку товара по макету с разделительной линией."""
    genre = product[1]         
    name = product[2]          
    duration = product[3]      
    price = product[4]         
    qty = product[5]           
    poster_name = product[6]   

    # ЗАДАНИЕ 1.2: Если количество <= 3, фон строго светло-красный, иначе белый
    # (В вашей БД у фильма "Оно" количество равно 3 — он подсветится)
    bg_color = "#ff8080" if qty <= 3 else "white"

    # ЗАДАНИЕ 1.1: Карточка с линией снизу (используем highlight-границы для создания линии)
    card = tk.Frame(parent, bg=bg_color, bd=0, 
                    highlightbackground="#CCCCCC", highlightthickness=1)
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = f"resources/{poster_name}" if poster_name else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 140))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[ПОСТЕР]", bg=bg_color, width=10, height=7).pack()

    # === Текстовая часть ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    title = f"{duration} мин. | {name}"
    tk.Label(text_frame, text=title, font=(FONT_FAMILY, 14, "bold"), bg=bg_color, anchor="w").pack(fill="x")
    tk.Label(text_frame, text=f"Жанр: {genre}", font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")
    
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"В наличии: {indicator} ({qty} шт.)", font=(FONT_FAMILY, 11), bg=bg_color, anchor="w").pack(fill="x")
    tk.Label(text_frame, text=f"Цена: {price} руб.", font=(FONT_FAMILY, 14, "bold"), bg=bg_color, anchor="e").pack(fill="x")

    return card
