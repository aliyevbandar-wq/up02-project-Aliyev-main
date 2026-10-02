"""Модели данных для проекта УП.02."""
from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (Фильм)."""

    def __init__(self, product_id, name, category, price, quantity):
        self.id = product_id
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

    def indicator(self):
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )
