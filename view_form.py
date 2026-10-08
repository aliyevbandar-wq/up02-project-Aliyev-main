import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os  # Добавили импорт os для безопасной проверки наличия иконки

from styles import font, COLOR_MAIN_BG, FONT_SIZE_HEADER, FONT_SIZE_NORMAL
from resources import get_product_image
from error_handler import safe_call


class ViewForm:
    def __init__(self, parent, product):
        self.parent = parent
        self.product = product
        
        # Создаем Toplevel окно (поверх главного)
        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр товара: {product[2] if product else '[Без названия]'}")
        self.window.geometry("500x650")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()  # Делаем окно модальным

        # ✨ СТРОКА ДЛЯ ЗАМЕНЫ ИКОНКИ (ВМЕСТО ПЕРА) ✨
        # Метод iconbitmap меняет иконку в заголовке окна на ваш файл .ico
        icon_path = "resources/icon.ico"
        if os.path.exists(icon_path):
            try:
                self.window.iconbitmap(icon_path)
            except Exception:
                # Если формат .ico не поддерживается ОС, используем PhotoImage
                try:
                    icon_img = tk.PhotoImage(file=icon_path)
                    self.window.iconphoto(False, icon_img)
                except Exception:
                    pass

        # Распаковка данных из кортежа/списка product по индексам вашей БД
        self.product_id = product[0]
        self.category = product[1] if product[1] else "Не указана"
        self.name = product[2] if product[2] else "[Без наименования]"
        
        raw_duration = product[3] if product[3] else 0
        self.duration = f"{raw_duration} мин." if isinstance(raw_duration, int) else str(raw_duration)
        
        self.price = product[4] if product[4] is not None else 0
        
        # Путь к вашей гифке
        self.gif_path = f"resources/{product[6]}" if product[6] else ""
        
        self.production = product[7] if len(product) > 7 and product[7] else "Россия"
        self.sizes = product[8] if len(product) > 8 and product[8] else "S, M, L, XL"

        # Списки и переменные для анимации
        self.frames = []
        self.frame_index = 0
        self.animation_job = None

        self._build_ui()

    def _build_ui(self):
        # Контейнер для изображения/анимации
        img_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        img_frame.pack(pady=15)
        
        # Метка, в которой будет крутиться гифка
        self.img_label = tk.Label(img_frame, bg=COLOR_MAIN_BG)
        self.img_label.pack()

        # Запуск считывания и анимации гифки
        self._load_and_animate_gif()

        # Контейнер для текстовой информации
        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG, padx=20)
        info_frame.pack(fill="x", expand=True)

        # Вывод данных на форму
        self._add_info_row(info_frame, "Наименование:", self.name, is_header=True)
        self._add_info_row(info_frame, "Категория:", self.category)
        self._add_info_row(info_frame, "Производство:", self.production)
        self._add_info_row(info_frame, "Длительность:", self.duration)
        self._add_info_row(info_frame, "Доступные размеры:", self.sizes)
        self._add_info_row(info_frame, "Цена:", f"{self.price} руб.", is_price=True)

        # Нижняя панель для кнопок
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG, pady=20)
        btn_frame.pack(side="bottom", fill="x", padx=20)

        # Кнопка «Назад»
        back_btn = tk.Button(btn_frame, text="← Назад", font=font(FONT_SIZE_NORMAL),
                             bg="#CCCCCC", fg="black", bd=0, padx=15, pady=8, cursor="hand2",
                             command=self._go_back)
        back_btn.pack(side="left")

        # Кнопка «Добавить в заказ»
        order_btn = tk.Button(btn_frame, text="🛒 Добавить в заказ", font=font(FONT_SIZE_NORMAL, bold=True),
                              bg="#70B2AF", fg="white", bd=0, padx=15, pady=8, cursor="hand2",
                              command=self._add_to_order_clicked)
        order_btn.pack(side="right")

    def _load_and_animate_gif(self):
        """Загружает статичное изображение или все кадры GIF-файла в зависимости от расширения."""
        if not self.gif_path:
            self._show_stub()
            return

        # 🟢 ПРОВЕРКА: Если файл — это гифка, запускаем анимацию
        if self.gif_path.lower().endswith('.gif'):
            try:
                idx = 0
                while True:
                    frame = tk.PhotoImage(file=self.gif_path, format=f"gif -index {idx}")
                    self.frames.append(frame)
                    idx += 1
            except tk.TclError:
                pass

            if self.frames:
                self._update_gif_frame()
                return
            else:
                self._show_stub()
                return

        # 🟢 ЕСЛИ НЕ ГИФКА (PNG/JPG): Загружаем как обычное статичное фото
        else:
            photo = get_product_image(self.gif_path, size=(150, 200))
            if photo:
                self.img_label.configure(image=photo, text="") # Очищаем текст заглушки
                self.img_label.__dict__['image'] = photo   # Защита от удаления картинки мусорщиком Python
            else:
                self._show_stub()


    def _update_gif_frame(self):
        """Циклически меняет кадры анимации по таймеру."""
        if not self.window.winfo_exists():
            return

        current_frame = self.frames[self.frame_index]
        self.img_label.configure(image=current_frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.animation_job = self.window.after(100, self._update_gif_frame)

    def _show_stub(self):
        """Отрисовывает заглушку, если анимация отсутствует."""
        self.img_label.configure(text="📷\nНет анимации", font=font(FONT_SIZE_NORMAL, bold=True),
                                 fg="#777777", bg="#EAEAEA", bd=1, relief="solid", width=16, height=9)

    def _add_info_row(self, parent, label_text, value_text, is_header=False, is_price=False):
        """Вспомогательный метод для красивой отрисовки строк данных."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG, pady=4)
        row.pack(fill="x")
        
        lbl = tk.Label(row, text=label_text, font=font(FONT_SIZE_NORMAL, bold=True), fg="#555555", bg=COLOR_MAIN_BG, width=18, anchor="w")
        lbl.pack(side="left")
        
        val_size = FONT_SIZE_HEADER if (is_header or is_price) else FONT_SIZE_NORMAL
        val_color = "#2B6CB0" if is_price else "black"
        
        val = tk.Label(row, text=value_text, font=font(val_size, bold=is_header or is_price), fg=val_color, bg=COLOR_MAIN_BG, anchor="w", justify="left", wraplength=280)
        val.pack(side="left", fill="x", expand=True)

    def _go_back(self):
        """Закрывает окно и сбрасывает фоновый поток таймера."""
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
        self.window.destroy()

    def _add_to_order_clicked(self):
        """Обработчик кнопки заказа через безопасный вызов."""
        safe_call(self._process_order)

    def _process_order(self):
        """Логика добавления товара."""
        messagebox.showinfo("Успех", f"Товар '{self.name}' успешно добавлен в ваш заказ!")
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
        self.window.destroy()
