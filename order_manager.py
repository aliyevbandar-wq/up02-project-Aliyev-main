"""Работа с заказами."""
import sqlite3
from datetime import datetime
import os

def get_connection():
    """Соединение с БД (с автоматическим подбором правильного пути)."""
    db_name = "db_variant_14.db"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Проверяем основной путь внутри папки database
    target_path = os.path.join(base_dir, "database", db_name)
    
    # Если там файла нет, подключаемся к корню проекта
    if not os.path.exists(target_path):
        target_path = os.path.join(base_dir, db_name)
        
    if not os.path.exists(target_path):
        target_path = os.path.join("database", db_name)
        
    return sqlite3.connect(target_path)


def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в БД.
    :param client: ФИО клиента
    :param product_id: id товара
    :param quantity: количество
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # 📌 ЗАДАНИЕ 6.2: Автоматическая фиксация текущей даты
    дата = datetime.now().strftime("%Y-%m-%d")
    
    cur.execute(
        'INSERT INTO "Заказ" (дата, клиент, товар_id, количество) VALUES (?, ?, ?, ?)',
        (дата, client, product_id, quantity)
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
    
    # Автоматически считываем имя таблицы, чтобы не было конфликтов кодировки кириллицы
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall() if r[0] != 'sqlite_sequence']
    target_table = "Товар"
    for table in tables:
        if "вар" in table.lower() or "товар" in table.lower() or "product" in table.lower():
            target_table = table
            break

    cur.execute(f'SELECT количество FROM "{target_table}" WHERE id = ?', (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0
