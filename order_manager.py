"""Работа с заказами."""
import sqlite3
from datetime import datetime

def get_connection():
    """Соединение с БД."""
    # Указываем правильный путь к базе данных внутри папки database
    return sqlite3.connect("database/db_variant_14.db")


def add_order_to_db(client, product_id, quantity):
    """Добавляет новый заказ в БД."""
    conn = get_connection()
    cur = conn.cursor()
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    cur.execute(
        'INSERT INTO "Заказ" (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)',
        (current_date, client, product_id, quantity)
    )
    
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id


def update_product_quantity(product_id, new_quantity):
    """Обновляет количество товара в БД."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        'UPDATE "Товар" SET количество = ? WHERE id = ?',
        (new_quantity, product_id)
    )
    
    conn.commit()
    conn.close()


def get_last_order_id():
    """Возвращает id последнего заказа."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT MAX(id) FROM "Заказ"')
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT количество FROM "Товар" WHERE id = ?', (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0
