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


class ViewForm:
    def __init__(self, parent, product, on_add_to_order=None):
        self.parent = parent
        self.product = product
        self.on_add_to_order = on_add_to_order  
        
        self.window = tk.Toplevel(parent)
        self.window.title("Просмотр товара")
        self.window.geometry("520x750")  
        self.window.configure(bg=COLOR_MAIN_BG)
        self.window.grab_set()  

        # Прямое извлечение по реальным индексам вашей БД
        self.product_id = product[0]
        self.category = product[1] if product[1] else "Не указана"
        self.name = product[2] if product[2] else "[Без наименования]"
        
        raw_duration = product[3] if product[3] else 0
        self.duration = f"{raw_duration} мин." if isinstance(raw_duration, int) else str(raw_duration)
        
        self.price = product[4] if product[4] is not None else 0
        
        # Индекс 6 отвечает за картинку-постер
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

        qty_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG, pady=10)
        qty_frame.pack(fill="x")
        
        qty_lbl = tk.Label(qty_frame, text="Количество:", font=font(FONT_SIZE_NORMAL, bold=True), 
                           fg="#555555", bg=COLOR_MAIN_BG, width=18, anchor="w")
        qty_lbl.pack(side="left")
        
        self.qty_entry = tk.Entry(qty_frame, font=font(FONT_SIZE_NORMAL), width=10)
        self.qty_entry.insert(0, "1")  
        self.qty_entry.pack(side="left")

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
        
        # Если это GIF-анимация, крутим её по кадрам
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
            # Если это обычная статичная картинка (jpg/png), выводим её пропорционально
            photo = get_product_image(self.gif_path, size=(150, 200))
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
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        user_input = self.qty_entry.get()
        is_valid, result = validate_positive_int(user_input, "Количество")
        if not is_valid:
            messagebox.showwarning("Ошибка ввода", result)
            return

        try:
            product_id = self.product_id
            current_qty = get_product_quantity(product_id)
            
            if current_qty < 1:
                messagebox.showwarning("Внимание", "Товар закончился")
                return
            
            new_qty = current_qty - 1
            add_order_to_db("Иванов Иван Иванович", product_id, 1)
            update_product_quantity(product_id, new_qty)
            
            messagebox.showinfo("Успех", "Заказ оформлен")
            
            if self.on_add_to_order:
                self.on_add_to_order()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при оформлении: {str(e)}")
