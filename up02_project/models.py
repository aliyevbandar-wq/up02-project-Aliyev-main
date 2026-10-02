"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар (подходит также для медиа: фильмы, спектакли и т.п.)."""

    def __init__(
        self,
        product_id,
        name,
        category,
        price,
        quantity,
        genre=None,
        duration_minutes=None,
        poster_url=None,
        manufacturer=None,
        composition=None,
        size=None,
    ):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: название
        :param category: категория
        :param price: цена
        :param quantity: количество
        :param genre: жанр (для медиа)
        :param duration_minutes: длительность в минутах (для медиа)
        :param poster_url: ссылка/путь к постеру
        :param manufacturer: производитель
        :param composition: состав
        :param size: размер
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.genre = genre
        self.duration_minutes = duration_minutes
        self.poster_url = poster_url
        self.manufacturer = manufacturer
        self.composition = composition
        self.size = size

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        """Строка с информацией о товаре (с учётом дополнительных полей)."""
        base = (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )

        parts = [base]

        if self.genre:
            parts.append(f"жанр: {self.genre}")
        if self.duration_minutes is not None:
            parts.append(f"длительность: {self.duration_minutes} мин")
        if self.poster_url:
            parts.append(f"постер: {self.poster_url}")
        if self.manufacturer:
            parts.append(f"производитель: {self.manufacturer}")
        if self.composition:
            parts.append(f"состав: {self.composition}")
        if self.size:
            parts.append(f"размер: {self.size}")

        return "; ".join(parts)
