"""Главное окно приложения с каталогом."""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # type: ignore
import os

from config import APP_TITLE, FONT_FAMILY
import db_loader as db  
from catalog import create_product_card


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("950x750")
        self.build_ui()
        self.load_products()

    def build_ui(self):
        # Шапка каталога
        header = tk.Frame(self.root, bg="#D2F6E7")
        header.pack(fill="x", side="top")

        # 📌 ЗАДАНИЕ 2: Добавление логотипа компании
        logo_path = "resources/logo.png"
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path).resize((50, 50))
                logo_photo = ImageTk.PhotoImage(logo)
                logo_label = tk.Label(header, image=logo_photo, bg="#D2F6E7")
                logo_label.__dict__['image'] = logo_photo
                logo_label.pack(side="left", padx=15, pady=10)
            except Exception:
                tk.Label(header, text="[LOGO]", bg="#D2F6E7").pack(side="left", padx=15)
        else:
            tk.Label(header, text="[LOGO]", bg="#D2F6E7").pack(side="left", padx=15)

        # Текст заголовка
        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg="#D2F6E7").pack(side="left", pady=15)

        # Область с прокруткой (Canvas)
        container = tk.Frame(self.root, bg="white")
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(self.canvas_window, width=event.width))
        self.catalog_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

    def load_products(self):
        products = db.get_all_products()
        if not products:
            tk.Label(self.catalog_frame, text="⚠ В базе данных не найдено товаров!",
                     font=(FONT_FAMILY, 12, "bold"), fg="red", bg="white").pack(pady=50)
            return

        for p in products:
            create_product_card(self.catalog_frame, p)
            
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()
