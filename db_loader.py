"""Загрузчик данных и работа с продуктами БД."""
import sqlite3
import os

def get_all_products():
    """Получает все фильмы из вашей таблицы, проверяя точные папки проекта."""
    db_name = "db_variant_14.db"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 📌 ПРОВЕРЯЕМ ПУТИ:
    # 1. Сначала ищем в папке database (как на вашем самом первом скриншоте)
    target_path = os.path.join(base_dir, "database", db_name)
    
    # 2. Если там нет, ищем в корне папки проекта
    if not os.path.exists(target_path):
        target_path = os.path.join(base_dir, db_name)
        
    # 3. Если и там нет, проверяем относительный путь
    if not os.path.exists(target_path):
        target_path = os.path.join("database", db_name)

    conn = sqlite3.connect(target_path)
    cursor = conn.cursor()
    
    # Автоматически считываем реальное имя таблицы, чтобы избежать проблем с кодировкой кириллицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if row[0] != 'sqlite_sequence']
    
    target_table = "Товар"  # значение по умолчанию
    for table in tables:
        if "вар" in table.lower() or "товар" in table.lower() or "product" in table.lower():
            target_table = table
            break
    if not target_table and tables:
        target_table = tables[0]
        
    # Считываем данные из таблицы
    cursor.execute(f'SELECT * FROM "{target_table}" ORDER BY id')
    products = cursor.fetchall()
    
    conn.close()
    return products


def get_products():
    """Резервный метод для совместимости."""
    return get_all_products()


def get_product_sizes(product_id):
    """Возвращает список размеров для товара."""
    return ["2D", "3D", "IMAX"]
