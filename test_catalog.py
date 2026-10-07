"""Расширенная проверка корректности данных каталога."""
import db_loader as db


def test_catalog_extended():
    """Проводит комплексное тестирование полей базы данных."""
    products = db.get_all_products()
    print(f"--- СТАРТ ТЕСТИРОВАНИЯ (Всего записей: {len(products)}) ---")
    
    if not products:
        print("❌ База данных пуста или не найдена!")
        return

    has_image_at_least_one = False
    price_errors = 0
    qty_errors = 0

    for p in products:
        # Извлекаем поля по вашим точным индексам:
        # id=p[0], цена=p[4], количество=p[5], постер=p[6]
        movie_id = p[0]
        price = p[4]
        qty = p[5]
        poster = p[6]

        # 1. Проверка: У всех товаров есть цена
        if price is None:
            print(f"❌ Фильм id={movie_id}: отсутствует цена")
            price_errors += 1

        # 2. Проверка: У всех товаров количество >= 0
        if qty is None or qty < 0:
            print(f"❌ Фильм id={movie_id}: недопустимое количество ({qty})")
            qty_errors += 1

        # 3. Проверка: Хотя бы у одного товара есть изображение
        if poster and poster.strip() != "" and poster != "picture.png":
            has_image_at_least_one = True

    # Вывод результатов
    if price_errors == 0:
        print("✅ У всех товаров есть цена (не None)")
        
    if qty_errors == 0:
        print("✅ У всех товаров количество >= 0")
        
    if has_image_at_least_one:
        print("✅ Хотя бы у одного товара есть изображение")
    else:
        print("❌ ОШИБКА: Ни у одного товара нет корректного изображения!")


if __name__ == "__main__":
    test_catalog_extended()
