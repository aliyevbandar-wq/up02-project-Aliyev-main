"""Каталог товаров (Фильмы)."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    # 🟢 ИСПРАВЛЕНО: Индекс количества в вашей БД равен 5
    qty = product[5]   
    bg_color = _get_card_color(qty)

    # Задание 1.1: Карточка с линией снизу (highlightbackground)
    card = tk.Frame(parent, bg=bg_color, bd=0, 
                    highlightbackground="#CCCCCC", highlightthickness=1)
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или улучшенную заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # 🟢 ИСПРАВЛЕНО: Индекс имени файла постера в вашей БД равен 6
    poster_name = product[6]
    image_path = f"resources/{poster_name}" if poster_name else ""

    photo = get_product_image(image_path, size=(100, 140))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.__dict__['image'] = photo   # Запись без ошибок Pylance
        img_label.pack()
    else:
        # 📌 УЛУЧШЕННАЯ ЗАГЛУШКА: Иконка фотоаппарата и текст "Нет фото"
        tk.Label(img_frame, 
                 text="📷\nНет фото", 
                 font=font(FONT_SIZE_NORMAL, bold=True), 
                 fg="#777777", 
                 bg="#F0F0F0", 
                 bd=1, 
                 relief="solid", 
                 width=12, 
                 height=7).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию с обработкой сложных крайних случаев."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Базовая валидация пустых значений (Задание 5.4)
    genre = product[1] if product[1] else "[Без жанра]"
    raw_name = product[2] if product[2] else "[Без названия]"
    duration = product[3] if product[3] else "[Без длительности]"
    raw_price = product[4] if product[4] is not None else 0

    # 📌 ЗАДАНИЕ 2: Обработка новых крайних случаев
    
    # 1. Защита от очень длинного названия (> 100 символов) — обрезаем с троеточием
    # Это предотвратит размывание или уползание верстки карточки за границы экрана
    name = (raw_name[:97] + "...") if len(raw_name) > 100 else raw_name

    # 2. Форматирование цены больше 1 000 000 руб.
    # Если цена огромная, пишем сокращенно "млн руб.", чтобы текст поместился в макет
    if raw_price >= 1000000:
        price_text = f"{raw_price / 1000000:.1f} млн руб."
    else:
        price_text = f"{raw_price} руб."

    # 3. Кириллические названия поддерживаются автоматически встроенными шрифтами Tkinter,
    # но для надежности мы гарантируем вывод через f-строки.

    # Отрисовка элементов
    duration_text = f"{duration} мин." if isinstance(duration, int) else duration
    _add_label(text_frame, f"{duration_text} | {name}", bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Жанр: {genre}", bg_color)
    _add_label(text_frame, f"В наличии: {_indicator(qty)} ({qty} шт.)", bg_color)
    
    # Нижняя панель для цены и кнопки
    bottom_frame = tk.Frame(text_frame, bg=bg_color)
    bottom_frame.pack(fill="x", side="bottom", pady=5)
    
    # Цена с поддержкой форматирования миллионных сумм
    tk.Label(bottom_frame, text=f"Цена: {price_text}", 
             font=font(FONT_SIZE_HEADER, bold=True), bg=bg_color).pack(side="left")
    
    # Кнопка действия
    tk.Button(bottom_frame, text="Купить билет", 
              font=font(FONT_SIZE_NORMAL, bold=True), 
              bg="#70B2AF", fg="white", 
              activebackground="#5A9390", activeforeground="white",
              bd=0, padx=15, pady=5, cursor="hand2").pack(side="right")



def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """Вспомогательная микрофункция для добавления стандартной текстовой метки."""
    tk.Label(parent, text=text, font=font(size, bold=bold),
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """Индикатор «много/мало» (порог 5)."""
    return "много" if qty > 5 else "мало"
