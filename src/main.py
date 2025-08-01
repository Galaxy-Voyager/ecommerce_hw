from __future__ import annotations


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название товара должно быть непустой строкой")
        if not isinstance(description, str):
            raise ValueError("Описание должно быть строкой")
        if not isinstance(price, (int, float)):
            raise ValueError("Цена должна быть числом")
        if not isinstance(quantity, int):
            raise ValueError("Количество должно быть целым числом")
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

        self.name = name.strip()
        self.description = description
        self._price = float(price)
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        # Доп. задание: подтверждение снижения цены
        if hasattr(self, "_price") and new_price < self._price:
            confirm = input(
                f"Вы уверены, что хотите снизить цену с {
                    self._price} до {new_price}? (y/n): "
            )
            if confirm.lower() != "y":
                print("Изменение цены отменено")
                return
        self._price = new_price

    def __str__(self) -> str:
        desc = (
            self.description[:20] + "..."
            if len(self.description) > 20
            else self.description
        )
        return f"{self.name}, {desc}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', description='{self.description}', price={self.price}, quantity={self.quantity})"

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: list[Product] | None = None
    ):
        """Создает новый продукт из словаря с валидацией данных."""
        # Проверка обязательных полей
        required_fields = ["name", "description", "price", "quantity"]
        if not all(field in product_data for field in required_fields):
            raise ValueError("Отсутствуют обязательные поля в данных продукта")

        # Основная реализация
        product = cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

        # Дополнительное задание: проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name == product.name:
                    existing_product.quantity += product.quantity
                    if existing_product.price < product.price:
                        existing_product.price = product.price
                    return existing_product
        return product


class Category:
    """
    Класс для представления категорий товаров.
    Содержит счетчики общего количества категорий и товаров.
    """

    # Счетчики класса (общие для всех экземпляров)
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list["Product"]):
        """
        Инициализация категории с полной валидацией входных данных.

        Args:
            name: Название категории (непустая строка)
            description: Описание категории (непустая строка)
            products: Список объектов Product

        Raises:
            ValueError: Если переданы невалидные данные
        """
        # Валидация входных данных
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название категории должно быть непустой строкой")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Описание категории должно быть непустой строкой")
        if not isinstance(products, list):
            raise ValueError("Продукты должны быть списком")
        if not all(isinstance(p, Product) for p in products):
            raise ValueError("Все элементы списка должны быть объектами Product")

        # Установка атрибутов
        self.name = name.strip()
        self.description = description.strip()
        self._products = products.copy()  # Используем копию списка для безопасности
        self._is_active = True

        # Обновление счетчиков
        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        """Строковое представление категории"""
        return f"{self.name}, количество продуктов: {len(self._products)}"

    def __repr__(self) -> str:
        """Формальное строковое представление для отладки"""
        return (
            f"Category(name='{self.name}', "
            f"description='{self.description}', "
            f"products_count={len(self.products)})"
        )

    def remove_category(self):
        """
        Уменьшает счетчики при удалении категории.
        Возвращает True при успешном удалении.
        Вызывает ValueError если категория уже удалена.
        """
        if not self._is_active:
            raise ValueError("Категория уже удалена")

        Category.category_count -= 1
        Category.product_count -= len(self._products)
        self._products = []
        self._is_active = False
        return True

    def add_product(self, product: "Product") -> None:
        """
        Добавляет товар в категорию.

        Args:
            product: Объект Product для добавления

        Raises:
            ValueError: Если передан не Product или товар уже есть в категории
        """
        if not isinstance(product, Product):
            raise ValueError("Можно добавлять только объекты Product")
        if product in self._products:
            raise ValueError("Товар уже есть в категории")

        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return self._products

    @products.setter
    def products(self, value):
        self._products = value

    @classmethod
    def reset_counters(cls) -> None:
        """Сбрасывает счетчики категорий и продуктов (для тестов)"""
        cls.category_count = 0
        cls.product_count = 0


def load_data_from_json(filename: str) -> list[Category]:
    """
    Загружает данные о категориях и товарах из JSON-файла.
    Полностью валидирует структуру данных и преобразует в объекты Python.

    Args:
        filename: Путь к JSON-файлу относительно корня проекта

    Returns:
        Список объектов Category с товарами

    Raises:
        ValueError: При ошибках в данных или файле
    """
    import json
    from pathlib import Path

    # 1. Валидация имени файла
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("Имя файла должно быть непустой строкой")

    try:
        # 2. Получение абсолютного пути
        file_path = Path(__file__).parent.parent / filename

        # 3. Чтение файла
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # 4. Валидация корневой структуры
        if not isinstance(data, list):
            raise ValueError("Ожидается список категорий")

        categories = []

        # 5. Обработка категорий
        for category_data in data:
            # 5.1. Проверка типа категории
            if not isinstance(category_data, dict):
                raise ValueError("Категория должна быть объектом")

            # 5.2. Проверка обязательных полей
            required = {"name", "description", "products"}
            if missing := required - set(category_data.keys()):
                raise ValueError(f"Отсутствуют поля: {missing}")

            # 5.3. Валидация продуктов
            if not isinstance(category_data["products"], list):
                raise ValueError("Продукты должны быть списком")

            products = []

            # 6. Обработка продуктов
            for product_data in category_data["products"]:
                try:
                    products.append(
                        Product(
                            name=str(product_data["name"]),
                            description=str(product_data["description"]),
                            price=float(product_data["price"]),
                            quantity=int(product_data["quantity"]),
                        )
                    )
                except (ValueError, TypeError, KeyError) as e:
                    raise ValueError(f"Ошибка в данных товара: {str(e)}")

            # 7. Создание категории
            try:
                categories.append(
                    Category(
                        name=str(category_data["name"]),
                        description=str(category_data["description"]),
                        products=products,
                    )
                )
            except ValueError as e:
                error_msg = f"Ошибка создания категории: {str(e)}"
                raise ValueError(error_msg)

        return categories

    except FileNotFoundError as e:
        raise ValueError(f"Файл не найден: {str(e)}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка JSON: {str(e)}")
    except Exception as e:
        raise ValueError(f"Ошибка обработки файла: {str(e)}")


if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)
