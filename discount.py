# discount.py
from datetime import timedelta

# --- ЗАГЛУШКА: имитация данных из таблицы «Заказ» ---
# В реальном проекте замени это на SQL-запрос к БД.
ORDERS_DB = [
    {"product_id": 1, "order_date": "2026-09-10"},
    {"product_id": 3, "order_date": "2026-09-20"},
    {"product_id": 1, "order_date": "2026-10-05"},
]

def _get_orders_for_product_in_period(product_id, start_date, end_date):
    """Возвращает список заказов на товар за период (заглушка)."""
    count = 0
    for order in ORDERS_DB:
        order_date = order["order_date"]
        # Простая проверка диапазона дат
        if order_date >= start_date.strftime("%Y-%m-%d") and order_date <= end_date.strftime("%Y-%m-%d"):
            if order["product_id"] == product_id:
                count += 1
    return count

def calculate_price_with_discount(product_id, price, date):
    """
    Рассчитывает цену со скидкой.
    Логика: если в предыдущем месяце не было заказов на товар → скидка 25%.
    """
    if price == 0:
        return 0

    # Определяем начало и конец предыдущего месяца относительно date
    # 1. Первый день текущего месяца
    first_day_current = date.replace(day=1)
    # 2. Последний день предыдущего месяца = первый день текущего - 1 день
    last_day_prev = first_day_current - timedelta(days=1)
    # 3. Первый день предыдущего месяца
    first_day_prev = last_day_prev.replace(day=1)

    # Проверяем наличие заказов в предыдущем месяце
    orders_count = _get_orders_for_product_in_period(product_id, first_day_prev, last_day_prev)

    if orders_count == 0:
        # Скидка 25%
        return int(price * 0.75)
    else:
        # Без скидки
        return price
