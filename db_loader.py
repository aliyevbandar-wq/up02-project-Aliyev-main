import sqlite3
import os
from config import DB_PATH

def get_all_products():
    """Получает все фильмы из вашей таблицы Товар."""
    if not os.path.exists(DB_PATH):
        print(f"Ошибка: Файл базы данных не найден по пути: {DB_PATH}")
        return []

    conn = sqlite3.connect(DB_PATH)
    
    # Настраиваем текстовый декодер на работу с любой кириллицей в SQLite
    conn.text_factory = lambda x: str(x, 'utf-8', 'ignore') if isinstance(x, bytes) else str(x)
    cursor = conn.cursor()
    
    try:
        # Прямой и точный запрос к вашей таблице 'Товар'
        cursor.execute('SELECT "id", "жанр", "название", "длительность", "цена", "количество", "постер" FROM "Товар"')
        products = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Ошибка при чтении таблицы Товар: {e}")
        products = []
        
    conn.close()
    return products
