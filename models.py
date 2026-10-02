"""Модели данных для проекта УП.02."""

class Product:
    """Класс Товар."""

    def __init__(self, product_id, name, category, price, quantity):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        """
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо)."""
        return self.price * 0.75
