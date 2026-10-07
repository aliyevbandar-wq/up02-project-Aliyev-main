"""Каталог товаров."""
import tkinter as tk
from tkinter import ttk
import os

# Импорт стилей по заданию 7.4
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER,
    font
)
from resources import get_product_image


def create_product_card(parent, product):
    """Создаёт карточку товара по макету с разделительной линией."""
    genre = product[1]         
    name = product[2]          
    duration = product[3]      
    price = product[4]         
    qty = product[5]           
    poster_name = product[6]   

    # Если количество <= 3, фон строго светло-красный из стилей, иначе белый
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG

    # Карточка с линией снизу
    card = tk.Frame(parent, bg=bg_color, bd=0, 
                    highlightbackground="#CCCCCC", highlightthickness=1)
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = f"resources/{poster_name}" if poster_name else ""

    # Подгружаем картинку через ресурсы по заданию 4.4
    photo = get_product_image(image_path, size=(100, 140))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo   
        img_label.pack()
    else:
        # 📌 ЗАМЕНИЛИ ЗДЕСЬ (Задание 1: Улучшенная заглушка)
        tk.Label(img_frame, 
                 text="📷\nНет фото", 
                 font=font(FONT_SIZE_NORMAL, bold=True), 
                 fg="#777777", 
                 bg="#F0F0F0", 
                 bd=1, 
                 relief="solid", 
                 width=12, 
                 height=7).pack()

    # === Текстовая часть ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    title = f"{duration} мин. | {name}"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color, anchor="w").pack(fill="x")
    tk.Label(text_frame, text=f"Жанр: {genre}", font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")
    
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"В наличии: {indicator} ({qty} шт.)", font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")
    
    # 📌 ДОБАВИЛИ КНОПКУ (Задание 2: применение цвета #70B2AF)
    # Создаем контейнер для нижней строчки с ценой и кнопкой
    bottom_frame = tk.Frame(text_frame, bg=bg_color)
    bottom_frame.pack(fill="x", side="bottom", pady=5)
    
    tk.Label(bottom_frame, text=f"Цена: {price} руб.", font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color).pack(side="left")
    
    # Кнопка фирменного цвета #70B2AF
    tk.Button(bottom_frame, text="Купить билет", 
              font=font(FONT_SIZE_NORMAL, bold=True), 
              bg="#70B2AF", fg="white", 
              activebackground="#5A9390", activeforeground="white",
              bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")

    return card
