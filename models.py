"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (Фильм)."""

    def __init__(self, product_id, name, category, price, quantity):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        """
        self.id = product_id  # Используем self.id для совместимости с price_with_discount_auto
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ."""
        if date is None:
            date = datetime.now()
        # Метод корректно передает 3 аргумента (id, базовая цена, дата)
        return calculate_price_with_discount(self.id, self.price, date)

    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо)."""
        return self.price * 0.90   # изменено в main

    def indicator(self):
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )


# Код для мгновенной проверки Задания 8.3 прямо при запуске файла
if __name__ == "__main__":
    p = Product(2, "Ботинки Timberland", "Ботинки", 15000, 3)
    date_test = datetime(2026, 10, 15)
    print("=" * 40)
    print("ПРОВЕРКА ИНТЕГРАЦИИ В КЛАСС PRODUCT")
    print("=" * 40)
    print(f"Базовая цена: {p.price}")
    print(f"Со скидкой: {p.price_with_discount_auto(date_test)}")
    print(f"Упрощенная скидка (25%): {p.discounted_price()}")
    print("=" * 40)
