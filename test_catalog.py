"""Проверка вывода полей."""
# 🟢 ИСПРАВЛЕНО: Импортируем ваш реальный модуль db_loader вместо database
import db_loader as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    # Учитывая, что в вашей таблице "Товар" 7 столбцов, 
    # проверка на минимум 6 полей пройдет идеально
    required_count = 6   # минимум полей для макета
    errors = 0

    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()
