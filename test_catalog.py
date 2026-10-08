"""Тестирование каталога."""
import db_loader as db


def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    try:
        products = db.get_all_products()
        return len(products) > 0
    except Exception:
        return False


def test_product_fields():
    """Проверяет, что у всех товаров достаточно полей."""
    try:
        products = db.get_all_products()
        for p in products:
            if len(p) < 7:
                print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
                return False
        return True
    except Exception:
        return False


def test_prices_are_numbers():
    """Проверяет, что все цены — числа."""
    try:
        products = db.get_all_products()
        for p in products:
            if not isinstance(p[4], (int, float)):
                print(f"❌ Товар id={p[0]}: цена не число ({p[4]})")
                return False
        return True
    except Exception:
        return False


def test_quantity_not_negative():
    """Проверяет, что количество не отрицательное."""
    try:
        products = db.get_all_products()
        for p in products:
            if p[5] < 0:
                print(f"❌ Товар id={p[0]}: отрицательное количество ({p[5]})")
                return False
        return True
    except Exception:
        return False


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название (Задание 6.6)."""
    try:
        products = db.get_all_products()
        for p in products:
            if not p[2] or str(p[2]).strip() == "":   
                print(f"❌ Товар id={p[0]}: пустое название")
                return False
        return True
    except Exception:
        return False


# 🟢 НОВЫЙ ТЕСТ: ПРОВЕРКА ИЗОБРАЖЕНИЙ (Задание 2)
def test_at_least_one_image_exists():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    try:
        products = db.get_all_products()
        for p in products:
            # Индекс 6 — имя файла постера (например, 'avatar.png')
            if len(p) > 6 and p[6] and str(p[6]).strip() != "":
                return True  # Как только нашли хотя бы один постер — тест успешно сдан
        
        print("❌ Ни у одного фильма в базе данных нет изображения!")
        return False
    except Exception:
        return False


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("У всех товаров есть название", test_names_not_empty),
        
        # 🟢 Добавлен в общий список тестов (Задание 2)
        ("Хотя бы у одного товара есть изображение", test_at_least_one_image_exists),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА (РАСШИРЕННОЕ)")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()
