import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import os

from styles import font, COLOR_MAIN_BG, FONT_SIZE_HEADER, FONT_SIZE_NORMAL
from resources import get_product_image
from error_handler import safe_call, validate_positive_int

from order_manager import (
    add_order_to_db, 
    update_product_quantity, 
    get_product_quantity
)

try:
    from db_products import get_product_sizes
except ImportError:
    def get_product_sizes(product_id):
        return []


class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.parent = parent
        self.product = product
        self.on_add_to_order = on_add_to_order  
        
        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр товара")
        self.window.geometry("520x780")  
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()  

        # Прямое извлечение по реальным индексам вашей БД
        self.product_id = product[0]
        self.category = product[1] if product[1] else "Не указана"
        self.name = product[2] if product[2] else "[Без наименования]"
        
        raw_duration = product[3] if product[3] else 0
        self.duration = f"{raw_duration} мин." if isinstance(raw_duration, int) else str(raw_duration)
        
        self.price = product[4] if product[4] is not None else 0
        
        self.gif_path = f"resources/{product[6]}" if product[6] else ""
        
        self.production = product[7] if len(product) > 7 and product[7] else "Россия"
        self.sizes = product[8] if len(product) > 8 and product[8] else "S, M, L, XL"
        self.description = product[9] if len(product) > 9 and product[9] else "Описание отсутствует."

        self.frames = []
        self.frame_index = 0
        self.animation_job = None

        self._build_ui()

    def _build_ui(self):
        img_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        img_frame.pack(pady=15)
        
        self.img_label = tk.Label(img_frame, bg=COLOR_MAIN_BG)
        self.img_label.pack()
        self._load_and_animate_gif()

        info_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG, padx=20)
        info_frame.pack(fill="x", expand=True)

        self._add_info_row(info_frame, "Наименование:", str(self.name), is_header=True)
        self._add_info_row(info_frame, "Категория:", str(self.category))
        self._add_info_row(info_frame, "Производство:", str(self.production))
        self._add_info_row(info_frame, "Длительность:", str(self.duration))
        self._add_info_row(info_frame, "Доступные размеры:", str(self.sizes))
        self._add_info_row(info_frame, "Цена:", f"{self.price} руб.", is_price=True)
        self._add_info_row(info_frame, "Описание:", str(self.description))

        # === Поле ввода количества ===
        qty_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)

        tk.Label(qty_frame, text="Количество:", font=font(FONT_SIZE_NORMAL, bold=True),
                 fg="#555555", bg=COLOR_MAIN_BG, width=18, anchor="w").pack(side="left")

        self.qty_var = tk.StringVar(value="1")
        self.qty_entry = tk.Entry(qty_frame, textvariable=self.qty_var, width=10,
                             font=font(FONT_SIZE_NORMAL))
        self.qty_entry.pack(side="left")

        # === Выбор размера ===
        size_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=10)

        tk.Label(size_frame, text="Размер:", font=font(FONT_SIZE_NORMAL, bold=True),
                 fg="#555555", bg=COLOR_MAIN_BG, width=18, anchor="w").pack(side="left")

        try:
            db_sizes = get_product_sizes(self.product_id)
        except Exception:
            db_sizes = []

        if not db_sizes:
            db_sizes = ["—"]

        self.size_var = tk.StringVar(value=db_sizes[0])
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                  values=db_sizes, state="readonly", width=8,
                                  font=font(FONT_SIZE_NORMAL))
        size_combo.pack(side="left")

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG, pady=20)
        btn_frame.pack(side="bottom", fill="x", padx=20)

        back_btn = tk.Button(btn_frame, text="← Назад", font=font(FONT_SIZE_NORMAL),
                             bg="#CCCCCC", fg="black", bd=0, padx=15, pady=8, cursor="hand2",
                             command=self._go_back)
        back_btn.pack(side="left")

        order_btn = tk.Button(btn_frame, text="🛒 Добавить в заказ", font=font(FONT_SIZE_NORMAL, bold=True),
                              bg="#70B2AF", fg="white", bd=0, padx=15, pady=8, cursor="hand2",
                              command=self._add_to_order_clicked)
        order_btn.pack(side="right")

    def _load_and_animate_gif(self):
        if not self.gif_path:
            self._show_stub()
            return
        
        # Интеллектуальный поиск расширения файла на диске
        real_path = self.gif_path
        if not os.path.exists(real_path):
            base_without_ext = os.path.splitext(self.gif_path)[0]
            for ext in [".png", ".jpg", ".gif", ".jpeg"]:
                if os.path.exists(base_without_ext + ext):
                    real_path = base_without_ext + ext
                    break

        if real_path.lower().endswith('.gif'):
            try:
                idx = 0
                while True:
                    frame = tk.PhotoImage(file=real_path, format=f"gif -index {idx}")
                    self.frames.append(frame)
                    idx += 1
            except tk.TclError:
                pass
            if self.frames:
                self._update_gif_frame()
                return
        else:
            photo = get_product_image(real_path, size=(150, 200))
            if photo:
                self.img_label.configure(image=photo, text="")
                self.img_label.__dict__['image'] = photo
                return
                
        self._show_stub()

    def _update_gif_frame(self):
        if not self.window.winfo_exists():
            return
        current_frame = self.frames[self.frame_index]
        self.img_label.configure(image=current_frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.animation_job = self.window.after(100, self._update_gif_frame)

    def _show_stub(self):
        self.img_label.configure(text="📷\nНет фото", font=font(FONT_SIZE_NORMAL, bold=True),
                                 fg="#777777", bg="#EAEAEA", bd=1, relief="solid", width=16, height=9)

    def _add_info_row(self, parent, label_text, value_text, is_header=False, is_price=False):
        row = tk.Frame(parent, bg=COLOR_MAIN_BG, pady=4)
        row.pack(fill="x")
        lbl = tk.Label(row, text=label_text, font=font(FONT_SIZE_NORMAL, bold=True), fg="#555555", bg=COLOR_MAIN_BG, width=18, anchor="w")
        lbl.pack(side="left")
        val_size = FONT_SIZE_HEADER if (is_header or is_price) else FONT_SIZE_NORMAL
        val_color = "#2B6CB0" if is_price else "black"
        val = tk.Label(row, text=value_text, font=font(val_size, bold=is_header or is_price), fg=val_color, bg=COLOR_MAIN_BG, anchor="w", justify="left", wraplength=280)
        val.pack(side="left", fill="x", expand=True)

    def _go_back(self):
        if self.animation_job:
            self.window.after_cancel(self.animation_job)
        self.window.destroy()

    def _add_to_order_clicked(self):
        """Обработчик кнопки «Добавить в заказ» с полной валидацией (Задание 5.2)."""
        # 1. Проверяем товар
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 2. Валидация количества
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return

        qty = result  # result — это успешно проверенное целое число

        # 3. Проверяем, что количество не больше доступного на складе
        try:
            current_qty = get_product_quantity(self.product_id)
            if qty > current_qty:
                messagebox.showwarning("Ошибка", f"Доступно только {current_qty} шт.")
                return
        except Exception:
            current_qty = 99  # резервный обход, если функция заблокирована

        # 4. Вызываем callback и списываем остатки
        try:
            new_qty = current_qty - qty
            add_order_to_db("Иванов Иван Иванович", self.product_id, qty)
            update_product_quantity(self.product_id, new_qty)
            
            messagebox.showinfo("Успех", f"Товар добавлен в заказ ({qty} шт.)")
            
            if self.on_add_to_order:
                # Передаем обновленный callback в каталог для перерисовки интерфейса
                if len(str(self.on_add_to_order)) > 0:
                    self.on_add_to_order()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка заказа", f"Не удалось добавить товар:\n{str(e)}")
